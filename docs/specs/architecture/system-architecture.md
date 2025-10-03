# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────┐
│     Odoo Cloud (SaaS Platform)      │
│                                     │
│  ┌───────────────────────────────┐  │
│  │   Custom Label Print Module   │  │
│  │                               │  │
│  │  - MO Split Detection         │  │
│  │  - Lot Number Generation      │  │
│  │  - GS1 Barcode Creation       │  │
│  │  - ZPL Template Engine        │  │
│  │  - Print Job Manager          │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
                 │
                 │ HTTPS POST (JSON)
                 ▼
┌─────────────────────────────────────┐
│   Ubuntu Print Server (On-Premise)  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │   Flask API (Docker)          │  │
│  │                               │  │
│  │  - REST Endpoints             │  │
│  │  - Print Queue Manager        │  │
│  │  - Job Status Tracking        │  │
│  └───────────────────────────────┘  │
│                 │                   │
│  ┌───────────────────────────────┐  │
│  │   CUPS Print System           │  │
│  │                               │  │
│  │  - Printer Management         │  │
│  │  - Raw ZPL Transmission       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
                 │
                 │ USB / Network (ZPL)
                 ▼
         ┌───────────────┐
         │ Zebra Z230    │
         │ 300 DPI       │
         │ Thermal       │
         └───────────────┘
```

## Component Descriptions

### Odoo Custom Module (Cloud)
**Purpose**: Orchestrates label generation and print job submission

**Key Responsibilities**:
- Detect Manufacturing Order split events
- Generate unique lot numbers for each product unit
- Create GS1-128 compliant barcode data
- Populate ZPL templates with product data
- Submit print jobs to Flask server via HTTPS
- Track print job status and history
- Provide user interface for manual operations

**Technology**: Python, Odoo Framework, PostgreSQL

### Flask Print Server (Ubuntu)
**Purpose**: Bridge between Odoo and physical printers

**Key Responsibilities**:
- Expose REST API for print job submission
- Manage print job queue and prioritization
- Interface with CUPS for printer communication
- Monitor printer status and health
- Return job status to Odoo
- Handle errors and retries

**Technology**: Python, Flask/FastAPI, Docker, Redis/SQLite

### CUPS (Common Unix Printing System)
**Purpose**: Low-level printer management

**Key Responsibilities**:
- Manage Zebra Z230 printer connection
- Transmit raw ZPL data to printer
- Monitor printer status (online/offline, errors)
- Handle print queue at OS level

**Technology**: CUPS daemon, printer drivers

## Communication Flow

### Normal Print Flow
1. User splits MO in Odoo (e.g., into 200 boxes)
2. Odoo module detects split event
3. Module generates 200 unique lot numbers
4. Module creates GS1 barcode data for each label
5. Module populates ZPL template 200 times
6. Module sends HTTPS POST to Flask API with batch of 200 labels
7. Flask validates request and queues print job
8. Flask returns job ID to Odoo
9. Flask sends ZPL codes to CUPS
10. CUPS transmits to Zebra printer
11. Printer produces 200 labels
12. Flask updates job status to "completed"
13. Odoo polls for status and displays confirmation

### Error Handling Flow
- **Printer Offline**: Flask detects via CUPS, returns error to Odoo, job marked as failed
- **Network Error**: Odoo retries 3 times with exponential backoff
- **Partial Print**: Flask tracks progress, allows resume from last successful label

## Security Architecture
- HTTPS/TLS encryption for Odoo ↔ Flask communication
- API key authentication on all Flask endpoints
- IP whitelist for Odoo server
- Rate limiting to prevent abuse
- Odoo role-based access control for print operations

## Related Documents
- [Data Flows](data-flows.md)
- [Technology Stack](technology-stack.md)
- [Flask API Specification](../reference/api-spec.md)