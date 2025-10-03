# Shun Printer - Design Decision Document

## Executive Summary

This document captures the architectural redesign of Shun's label printing system, pivoting from a Flask/Redis/RQ architecture to a simplified FastAPI-based system with PostgreSQL as the single source of truth. This tactical shift prioritizes simplicity, maintainability, and direct integration patterns while maintaining the core functionality of automated GS1-compliant label printing for catch weight products.

## Context for Redesign

### Original Architecture
- Flask REST API with Redis/RQ for job queuing
- Complex polling mechanism between Odoo and Flask
- Scattered state management across Odoo and Flask
- Template versioning system
- Multiple abstraction layers in Odoo models

### Current Reality
- Development phase (not yet in production)
- Single printer deployment (Zebra Z230, 300 DPI)
- ~5 concurrent users
- Print volumes: potentially thousands of labels per day in batches of ~200
- Odoo SaaS deployment (Odoo.com) with custom modules
- Ubuntu server on same LAN as printer

### Redesign Rationale
- **Simplification**: Remove unnecessary complexity (Redis, RQ, excessive abstraction)
- **Single Source of Truth**: PostgreSQL becomes authoritative for lot numbers and job state
- **Modern Stack**: FastAPI replaces Flask for better async support and auto-documentation
- **Observability**: Streamlit dashboard for operations monitoring
- **Maintainability**: Clearer separation of concerns, simpler codebase

## Core Design Decisions

### 1. FastAPI Over Flask

**Decision**: Replace Flask with FastAPI as the print server framework.

**Rationale**:
- Native async support for better concurrency
- Automatic OpenAPI documentation
- Built-in request/response validation with Pydantic
- Modern Python patterns (type hints, async/await)
- Better performance characteristics

**Trade-offs**:
- Learning curve for async patterns
- Slightly less mature ecosystem than Flask
- Requires Python 3.8+

### 2. PostgreSQL as Single Source of Truth

**Decision**: PostgreSQL becomes the authoritative source for lot numbers, job state, and print history.

**Schema Design**:
- `label_print` schema (not public)
- Every table has `id` (UUID), `created_at`, `updated_at`
- Soft deletes via `deleted_at` timestamp
- Separate `zpl_cache` table for generated ZPL code

**Rationale**:
- Eliminates state synchronization issues between Odoo and print server
- Provides clear audit trail
- Enables direct queries for debugging and reporting
- Survives service restarts

**Key Tables**:
```sql
label_print.jobs          -- Print job metadata and status
label_print.labels        -- Individual labels (1 per lot number)
label_print.zpl_cache     -- Generated ZPL code (14-day TTL, compressed)
```

**Trade-off**: Odoo may want to be source of truth for lot numbers (flagged in open questions).

### 3. Eliminate Redis/RQ Queue

**Decision**: Use FastAPI's built-in BackgroundTasks instead of Redis/RQ.

**Rationale**:
- Print volume doesn't justify distributed queue complexity
- ~5 concurrent users, ~200 labels per batch is manageable
- Simpler deployment (one less service)
- Faster iteration during development

**Limitations Accepted**:
- Jobs lost if FastAPI crashes mid-print (mitigated by retry logic)
- No distributed worker pool (not needed for single printer)
- Limited to single server (acceptable for MVP)

**Mitigation Strategy**:
- Implement "stuck job detector" cron to retry abandoned jobs
- PostgreSQL job state survives restarts
- Manual retry endpoint for failed jobs

### 4. Lot Number Generation in PostgreSQL

**Decision**: FastAPI/PostgreSQL generates lot numbers, not Odoo.

**API Pattern**:
```
POST /lot-numbers/reserve
  → Returns: {"lot_numbers": ["LOT-2025-000001", ...]}

Odoo:
1. Reserves 200 lot numbers from FastAPI
2. Creates stock.production.lot records in Odoo
3. Submits print job with pre-allocated lot numbers
```

**Rationale**:
- Single source of truth for lot number sequence
- Easier to handle partial print failures
- Clear ownership boundary
- PostgreSQL sequence guarantees uniqueness

**Format**: `LOT-YYYY-NNNNNN` (e.g., LOT-2025-000001)
- 6-digit zero-padded sequence
- Year-based prefix for readability
- Globally unique across all jobs

**Open Question**: Does Odoo require lot numbers to exist in `stock.production.lot` BEFORE printing, or can they be created retroactively?

### 5. Template Management Simplification

**Decision**: Templates are files on disk, not database records.

**Structure**:
```
fastapi/templates/
  default.zpl
  seafood_4x6.zpl
  meat_4x6.zpl
```

**Format**: Jinja2 templates with ZPL syntax
```zpl
^XA
^FO50,50^A0N,50,50^FD{{ product_name }}^FS
^FO50,120^BY3^BCN,100,Y,N,N^FD{{ lot_number }}^FS
^XZ
```

**Features**:
- Hot-reload: Templates reload on file modification
- Validation: Pydantic wrapper checks for required variables
- No versioning: Templates rarely change (per Shun)

**Rationale**:
- Shun is the only template editor
- Changes are infrequent
- Git provides version control
- Simpler than database-backed templates

**Eliminated**:
- Template versioning system (premature optimization)
- Odoo-based template management UI
- Database storage for templates

### 6. GS1 Barcode Generation

**Decision**: Simple Python library, not an Odoo model.

**Implementation**:
```python
def generate_gs1_barcode(
    gtin: str,
    lot_number: str,
    weight_kg: float,
    production_date: date,
    expiration_date: date | None = None
) -> str:
    """Generate GS1-128 data string"""
    # AI (01): GTIN-14
    # AI (10): Lot/Batch Number
    # AI (3103): Net Weight (3 decimal places)
    # AI (11): Production Date (YYMMDD)
    # AI (17): Expiration Date (YYMMDD)
```

**Rationale**:
- Barcode generation is pure computation
- No need for Odoo model abstraction
- Easier to test and maintain
- Can be used by both Odoo and FastAPI

**Open Questions**:
- Do we need GTIN check digit validation?
- Human-readable vs machine-readable formats?
- Any GS1 AIs beyond (01), (10), (3103), (11), (17)?

### 7. Status Updates: HTTP Polling

**Decision**: Odoo polls FastAPI every 1 minute for job status.

**Flow**:
```python
# Odoo cron job (every 60 seconds)
for job_id in active_jobs:
    status = requests.get(f"{api_url}/jobs/{job_id}")
    update_odoo_record(job_id, status)
```

**Rationale**:
- Simple to implement and debug
- Odoo SaaS has cron job support
- 1-minute latency is acceptable for print jobs
- No webhook infrastructure needed

**Limitations Accepted**:
- Not real-time (1-minute polling interval)
- Odoo misses updates if it's down (acceptable: "chill")
- Extra HTTP traffic (minimal at 1 req/min per active job)

**Future Enhancement**: FastAPI webhook to Odoo (if Odoo can expose endpoints)

### 8. Streamlit Admin Dashboard

**Decision**: Build minimal read-only dashboard in Streamlit.

**Scope**:
1. **Job List**: Recent jobs with filtering (status, date, MO reference)
2. **Job Details**: Individual job info, label status, retry option
3. **Printer Status**: Online/offline, last print, error count
4. **System Health**: Success rate, total jobs, average print time

**Features**:
- Read-only (no actions like retry/cancel)
- Manual refresh button (no real-time updates)
- No authentication (local network only)
- Direct PostgreSQL connection

**Rationale**:
- Operations team needs visibility without Odoo access
- Simple debugging interface
- Minimal development effort
- Easy to iterate on metrics

**Docker Integration**: Separate container in docker-compose, same network as PostgreSQL.

### 9. Docker Compose Architecture

**Decision**: Four-container deployment.

**Services**:
```yaml
services:
  postgres:     # Job state, lot numbers, history
  fastapi:      # Print server API
  cups:         # Printer management
  streamlit:    # Admin dashboard
```

**Network**:
- All containers on same Docker network
- FastAPI → CUPS via network (port 631)
- Streamlit → PostgreSQL via network (port 5432)
- FastAPI → PostgreSQL via network (port 5432)

**Volumes**:
- `postgres_data`: Database persistence
- `cups_config`: Printer configuration
- `./templates`: Hot-reloadable ZPL templates

**Rationale**:
- Clean separation of concerns
- Independent scaling (if needed)
- Easy to develop/test individual services
- Standard Docker patterns

### 10. Authentication: Simple JWT

**Decision**: Single JWT token shared by all Odoo users.

**Implementation**:
```python
Authorization: Bearer <jwt_token>
```

**Rationale**:
- Odoo SaaS deployment (all users trusted)
- No per-user tracking needed
- Simple to manage and rotate
- Sufficient for on-premise deployment

**Not Implemented**:
- Per-user JWT tokens
- OAuth2 flows
- API key rotation mechanisms

**Security Posture**:
- Ubuntu box behind firewall (same LAN as printer)
- Streamlit dashboard: local network only
- PostgreSQL: not exposed to internet

### 11. Error Handling Strategy

**Decision**: Fail fast with retry mechanisms.

**Retry Logic**:
- Automatic retry: Up to 3 attempts per label
- Exponential backoff: 1s, 2s, 4s
- Track failed labels in `labels.status = 'failed'`
- Manual retry endpoint: `POST /jobs/{job_id}/retry`

**Failure Scenarios** (flagged for Shun clarification):
- **Printer Offline**: Queue jobs, retry when online
- **Invalid ZPL**: Fail entire job or skip label?
- **Partial Print**: Job jams after 100 of 200 labels
  - Which lot numbers are "burned"?
  - Retry from label 101 or reprint all?

**Stuck Job Detection**:
- Cron job checks for jobs in "printing" status > 10 minutes
- Automatic transition to "failed" state
- Notification to Streamlit dashboard

### 12. Data Persistence Strategy

**What Gets Persisted**:
- ✅ Print job queue (survives restart)
- ✅ Print job history (auditing, 14-day retention for ZPL)
- ✅ Lot numbers (authoritative source)
- ✅ Printer configuration (database, not env vars)
- ❌ Templates (files on disk, Git for history)

**Retention Policy**:
- Jobs: Keep indefinitely (soft delete)
- Labels: Keep indefinitely (soft delete)
- ZPL Cache: 14-day TTL, compressed storage

**Soft Deletes**:
- `deleted_at TIMESTAMPTZ` column on all tables
- Queries filter: `WHERE deleted_at IS NULL`
- Allows data recovery and audit trails

## API Contract

### Core Endpoints

#### POST /lot-numbers/reserve
Reserve a batch of unique lot numbers.

**Request**:
```json
{
  "quantity": 200
}
```

**Response** (201):
```json
{
  "lot_numbers": ["LOT-2025-000001", ..., "LOT-2025-000200"],
  "reserved_at": "2025-10-02T14:25:00Z"
}
```

**Notes**:
- Lot numbers are immediately allocated (not reserved with expiry)
- Once allocated, they are "burned" even if not used
- No release endpoint (fire-and-forget pattern)

#### POST /jobs
Submit a new print job.

**Request**:
```json
{
  "mo_reference": "MO/2025/001",
  "product": {
    "sku": "SALM-001",
    "name": "Wild Caught Salmon",
    "gtin": "00012345678905"
  },
  "quantity": 200,
  "lot_numbers": ["LOT-2025-000001", ...],  // pre-allocated
  "weights": [1.250, 1.350, ...],           // array of 200 weights
  "production_date": "2025-10-02",
  "expiration_date": "2025-11-02",
  "template_name": "seafood_4x6",
  "metadata": {
    "user_id": "odoo_user_123",
    "company_name": "Shun Commissary"
  }
}
```

**Response** (201):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2025-10-02T14:25:00Z"
}
```

#### GET /jobs/{job_id}
Get current job status.

**Response** (200):
```json
{
  "job_id": "550e8400...",
  "status": "printing",  // queued | printing | completed | failed
  "progress": {
    "total": 200,
    "completed": 150,
    "failed": 0
  },
  "lot_numbers": [...],
  "created_at": "2025-10-02T14:25:00Z",
  "started_at": "2025-10-02T14:26:00Z",
  "completed_at": null,
  "error": null
}
```

#### POST /jobs/{job_id}/retry
Retry failed labels in a job.

**Request**:
```json
{
  "retry_all": false  // if false, only retry failed labels
}
```

**Response** (200):
```json
{
  "job_id": "550e8400...",
  "reprint_job_id": "660f9511...",  // new job for retries
  "labels_to_retry": 5
}
```

#### GET /health
Health check endpoint.

**Response** (200):
```json
{
  "status": "healthy",
  "database": "connected",
  "cups": "online",
  "printer": "ready"
}
```

## Database Schema

### Core Tables

```sql
CREATE SCHEMA label_print;

-- Print Jobs
CREATE TABLE label_print.jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mo_reference TEXT NOT NULL,
  product_sku TEXT NOT NULL,
  product_name TEXT NOT NULL,
  product_gtin TEXT,
  quantity INTEGER NOT NULL,
  status TEXT NOT NULL,  -- queued, printing, completed, failed
  template_name TEXT NOT NULL DEFAULT 'default',
  metadata JSONB,
  error_message TEXT,
  failed_count INTEGER DEFAULT 0,
  reprint_of_job_id UUID REFERENCES label_print.jobs(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ
);

-- Individual Labels
CREATE TABLE label_print.labels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID NOT NULL REFERENCES label_print.jobs(id) ON DELETE CASCADE,
  lot_number TEXT NOT NULL UNIQUE,
  box_number INTEGER NOT NULL,
  weight NUMERIC(10, 3) NOT NULL,
  weight_unit TEXT NOT NULL DEFAULT 'kg',
  production_date DATE NOT NULL,
  expiration_date DATE,
  status TEXT NOT NULL,  -- pending, printed, failed
  print_attempts INTEGER NOT NULL DEFAULT 0,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  printed_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ
);

-- ZPL Code Cache (14-day TTL, compressed)
CREATE TABLE label_print.zpl_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  label_id UUID NOT NULL REFERENCES label_print.labels(id) ON DELETE CASCADE,
  zpl_code TEXT NOT NULL,  -- compressed
  template_name TEXT NOT NULL,
  variables_used JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at TIMESTAMPTZ NOT NULL DEFAULT (now() + interval '14 days')
);

-- Indexes
CREATE INDEX idx_jobs_status ON label_print.jobs(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_jobs_created_at ON label_print.jobs(created_at);
CREATE INDEX idx_labels_job_id ON label_print.labels(job_id);
CREATE INDEX idx_labels_lot_number ON label_print.labels(lot_number) WHERE deleted_at IS NULL;
CREATE INDEX idx_labels_status ON label_print.labels(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_zpl_cache_label_id ON label_print.zpl_cache(label_id);
CREATE INDEX idx_zpl_cache_expires_at ON label_print.zpl_cache(expires_at);
```

### Lot Number Sequence

```sql
CREATE SEQUENCE label_print.lot_number_seq
  START WITH 1
  INCREMENT BY 1
  NO CYCLE;

-- Function to generate lot numbers
CREATE OR REPLACE FUNCTION label_print.generate_lot_number()
RETURNS TEXT AS $$
DECLARE
  seq_num INTEGER;
  year_str TEXT;
BEGIN
  seq_num := nextval('label_print.lot_number_seq');
  year_str := to_char(CURRENT_DATE, 'YYYY');
  RETURN 'LOT-' || year_str || '-' || lpad(seq_num::text, 6, '0');
END;
$$ LANGUAGE plpgsql;
```

## Project Structure

```
shun-printer/
├── docs/
│   ├── joshs_questions/
│   │   ├── DESIGN_DECISIONS.md       (this file)
│   │   └── OPEN_QUESTIONS.md
│   └── specs/                         (original specs, reference only)
├── fastapi/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Settings (Pydantic BaseSettings)
│   │   ├── database.py                # SQLAlchemy async setup
│   │   ├── models.py                  # SQLAlchemy models
│   │   ├── schemas.py                 # Pydantic schemas
│   │   ├── routers/
│   │   │   ├── jobs.py                # POST/GET /jobs
│   │   │   ├── lot_numbers.py         # POST /lot-numbers/reserve
│   │   │   └── health.py              # GET /health
│   │   ├── services/
│   │   │   ├── printer.py             # CUPS integration
│   │   │   ├── gs1.py                 # GS1 barcode generation
│   │   │   ├── templates.py           # Template loading + validation
│   │   │   └── background.py          # Background task runner
│   │   └── utils/
│   │       ├── zpl.py                 # ZPL helpers
│   │       └── auth.py                # JWT validation
│   ├── templates/
│   │   ├── default.zpl
│   │   └── seafood_4x6.zpl
│   ├── migrations/
│   │   └── 001_initial_schema.sql
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
├── streamlit/
│   ├── app.py                         # Main dashboard
│   ├── pages/
│   │   ├── 1_job_list.py
│   │   ├── 2_job_details.py
│   │   ├── 3_printer_status.py
│   │   └── 4_system_health.py
│   ├── Dockerfile
│   └── requirements.txt
├── odoo/
│   └── label_print/                   # Odoo module (to be designed)
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── models/
│       └── views/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Implementation Phases

### Phase 1: Core API (Days 1-2)
- FastAPI project setup
- PostgreSQL schema + migrations
- Basic CRUD for jobs and lot numbers
- Docker Compose configuration
- Health check endpoints

### Phase 2: Printing Logic (Days 3-4)
- CUPS integration (cups-connector library)
- Template loading with hot-reload
- GS1 barcode generation library
- Background task for printing
- Error handling + retry logic

### Phase 3: Observability (Day 5)
- Streamlit dashboard
- Job list + details views
- Printer status monitoring
- Basic metrics (success rate, print time)

### Phase 4: Odoo Integration (Days 6-7)
- JWT authentication
- Odoo module structure
- API client in Odoo (requests library)
- Polling cron job (1-minute interval)
- End-to-end testing

### Phase 5: Production Readiness (Day 8)
- Stuck job detector cron
- ZPL cache cleanup (14-day expiry)
- Logging configuration
- Deployment documentation

## Success Metrics

### Technical
- Print success rate: >95%
- API response time: <500ms (p99)
- Job processing time: <10 minutes for 200 labels
- System uptime: 99%+ (excluding planned maintenance)

### Operational
- Manual reprints: <5% of total prints
- Failed jobs requiring intervention: <2%
- Average time to resolve printer offline: <15 minutes

### Developer Experience
- Time to add new template: <5 minutes
- Time to debug failed job: <10 minutes
- Time to deploy updates: <10 minutes

## Risk Mitigation

### Job Loss on Crash
**Risk**: FastAPI crashes, in-flight jobs lost.
**Mitigation**: 
- Stuck job detector marks abandoned jobs as failed
- Manual retry endpoint for recovery
- PostgreSQL preserves job state

### Lot Number Conflicts
**Risk**: PostgreSQL sequence collision (extremely rare).
**Mitigation**:
- Database-level sequence is atomic
- UNIQUE constraint on lot_number
- Application-level retry with exponential backoff

### Printer Offline
**Risk**: Printer offline for extended period.
**Mitigation**:
- Jobs remain in "queued" state
- Stuck job detector transitions to "failed" after timeout
- Manual retry when printer returns
- Streamlit dashboard shows printer status

### Template Errors
**Risk**: Invalid ZPL causes print failures.
**Mitigation**:
- Template validation on load (check for required variables)
- Test print endpoint before production use
- ZPL cache allows inspection of generated code

## Open Questions (See OPEN_QUESTIONS.md)

Critical questions that require Shun's input:
1. Is PostgreSQL or Odoo the source of truth for lot numbers?
2. Does Odoo require lot numbers to exist before printing?
3. What happens to lot numbers if printing fails halfway?
4. Can Odoo expose webhook endpoints?
5. Detailed error handling scenarios (printer offline, invalid ZPL, partial prints)

## Appendix: Decisions NOT Made

These items are explicitly deferred or out of scope:

### Out of Scope
- Multiple printer support (future enhancement)
- Distributed queue (Redis/RQ)
- Template versioning system
- Real-time status updates (webhooks, SSE, WebSockets)
- Per-user authentication
- Scale integration (handled separately by Shun)
- Predictive print job scheduling
- Advanced analytics (beyond basic metrics)

### Explicitly Premature
- Template management UI in Odoo
- Complex retry strategies (exponential backoff with jitter)
- Job prioritization queues
- Audit logging for compliance
- Data warehouse integration

### Future Enhancements (Nice to Have)
- Webhook support for real-time updates
- Multiple printer load balancing
- Advanced failure prediction
- Integration with external monitoring (Prometheus, Grafana)
- Mobile app for operators

---

**Document Status**: Draft for Review  
**Last Updated**: 2025-10-02  
**Next Review**: After Shun clarifies open questions  
**Authors**: Joshua (architecture), Claude (documentation)