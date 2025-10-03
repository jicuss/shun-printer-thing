# Shun Printer - Open Questions for Shun

## Document Purpose

This document captures all questions that require Shun's input before finalizing the system design. Questions are organized by priority and category.

**Status**: Awaiting Shun's Response  
**Created**: 2025-10-02  
**Response Deadline**: TBD

---

## Critical Path Questions

These questions directly impact the core architecture and must be answered before implementation begins.

### 1. Source of Truth for Lot Numbers

**Question**: Should PostgreSQL or Odoo be the authoritative source of truth for lot numbers?

**Context**: Our current design has PostgreSQL generating and storing lot numbers, with Odoo receiving them after allocation. However, you may want Odoo's inventory system to be the source of truth.

**Two Options**:

**Option A: PostgreSQL as Source of Truth (current design)**
```
1. FastAPI generates lot numbers in PostgreSQL
2. Odoo calls POST /lot-numbers/reserve to get 200 lot numbers
3. Odoo creates stock.production.lot records with those numbers
4. Odoo submits print job with pre-allocated lot numbers
```

**Option B: Odoo as Source of Truth**
```
1. Odoo generates lot numbers internally
2. Odoo creates stock.production.lot records
3. Odoo submits print job with Odoo-generated lot numbers
4. FastAPI stores them in PostgreSQL for tracking
```

**Trade-offs**:
- **Option A**: Simpler failure handling, single sequence, easier to prevent duplicates
- **Option B**: Odoo inventory system remains authoritative, potentially required by Odoo's stock module

**Your Input Needed**: Which option aligns with Odoo's inventory requirements?

---

### 2. Lot Number Prerequisites

**Question**: Does Odoo's inventory system REQUIRE lot numbers to exist in `stock.production.lot` BEFORE the print job is submitted?

**Context**: This affects the workflow timing.

**Scenario A: Lot Numbers Must Exist First**
```
1. Generate/reserve lot numbers
2. Create stock.production.lot records in Odoo
3. Submit print job
4. Print labels
```

**Scenario B: Lot Numbers Can Be Created After**
```
1. Submit print job (FastAPI generates lot numbers)
2. Print labels
3. Create stock.production.lot records in Odoo retroactively
```

**Your Input Needed**: Which scenario matches Odoo's requirements?

---

### 3. Partial Print Failure Handling

**Question**: If a print job fails halfway through (e.g., printed 100 of 200 labels, then printer jams), what should happen to the lot numbers?

**Context**: This is critical for inventory accuracy and compliance.

**Scenarios to Consider**:

**Scenario 1: Labels 1-100 printed successfully, then jam**
- Are lot numbers LOT-2025-000001 through LOT-2025-000100 "burned" (already on physical labels)?
- When retrying, do we:
  - A) Start fresh with LOT-2025-000101 through LOT-2025-000200 (waste 100 numbers)
  - B) Resume with LOT-2025-000101 through LOT-2025-000200 (requires tracking which labels printed)
  - C) Reprint ALL 200 labels with new numbers (waste all 200 original numbers)

**Scenario 2: Uncertain which labels printed (power loss, communication failure)**
- Do we assume ALL printed or NONE printed?
- Manual intervention required?

**Your Input Needed**: 
1. Can we track which specific labels physically printed?
2. What's the business rule for "burned" lot numbers?
3. Is manual verification required for partial failures?

---

### 4. Odoo Webhook Capability

**Question**: Can Odoo SaaS (Odoo.com) expose HTTP endpoints for FastAPI to call?

**Context**: We're designing with HTTP polling (Odoo → FastAPI every 1 minute), but webhooks would be more efficient.

**Current Design (Polling)**:
```python
# Odoo cron job every 60 seconds
for job_id in active_jobs:
    status = requests.get(f"{fastapi_url}/jobs/{job_id}")
    update_odoo_record(job_id, status)
```

**Alternative (Webhook)**:
```python
# FastAPI calls Odoo when job completes
await httpx.post(
    f"{odoo_url}/api/print_job_webhook",
    json={"job_id": job_id, "status": "completed"}
)
```

**Your Input Needed**: 
1. Can you create HTTP endpoints in an Odoo SaaS module?
2. If yes, is webhook pattern preferred over polling?
3. If no, is 1-minute polling interval acceptable?

---

### 5. Manufacturing Order (MO) Split Mechanics

**Question**: What exactly happens in Odoo when a Manufacturing Order is split into multiple units?

**Context**: We need to understand the trigger point for label printing.

**Specific Questions**:
1. Does splitting create NEW `mrp.production` records, or modify existing ones?
2. Is there a specific state/status change we can detect?
3. Can we hook into a method like `action_split_production()`?
4. Are catch weights assigned BEFORE or DURING the split?
5. How many splits can occur? (e.g., can one MO be split multiple times?)

**Your Input Needed**: Walk us through the MO split workflow in your Odoo instance.

---

## GS1 Barcode Specifications

These questions clarify the exact GS1-128 barcode requirements.

### 6. GTIN Validation

**Question**: Do we need to validate GTIN check digits?

**Context**: GS1 GTINs have a check digit (digit 14) that validates the previous 13 digits.

**Options**:
- **Validate**: Reject invalid GTINs at job submission
- **Trust Odoo**: Assume Odoo's product master data is correct
- **Calculate**: Generate check digit if missing

**Your Input Needed**: Are your GTINs already validated in Odoo, or should FastAPI validate them?

---

### 7. Barcode Format Requirements

**Question**: Do you need human-readable format, machine-readable format, or both?

**Context**: 
- **Human-readable**: `(01)00012345678905(10)LOT-2025-000001(3103)001250`
- **Machine-readable**: Uses FNC1 characters, no parentheses

**Your Input Needed**: 
1. Which format does your Zebra printer require?
2. Do labels need to show both formats?
3. Are there specific printing requirements from your retailers/distributors?

---

### 8. Additional GS1 Application Identifiers

**Question**: Do you need any GS1 AIs beyond these?

**Currently Planned**:
- `(01)` GTIN-14
- `(10)` Lot/Batch Number
- `(3103)` Net Weight (3 decimal places in kg)
- `(11)` Production Date (YYMMDD)
- `(17)` Expiration Date (YYMMDD)

**Other Common AIs**:
- `(21)` Serial Number
- `(310n)` Weight with different decimal places
- `(7003)` Expiration Date + Time
- `(8020)` Pay Slip ID
- Custom AIs

**Your Input Needed**: Any additional AIs required by your business or retail partners?

---

## Error Handling Scenarios

These questions define the system's behavior in edge cases.

### 9. Printer Offline Duration

**Question**: If the printer is offline for hours or days, what should happen?

**Options**:
- **Queue indefinitely**: Jobs wait until printer returns (could be days)
- **Timeout after N hours**: Mark as failed, require manual retry
- **Alert immediately**: Notify user, but keep job queued

**Your Input Needed**: What's the maximum acceptable wait time before manual intervention?

---

### 10. Invalid ZPL Template

**Question**: If a template generates invalid ZPL code, should we fail the entire job or skip that label?

**Context**: Template errors are rare (only Shun edits them), but could happen.

**Options**:
- **Fail entire job**: Safest, ensures all labels are correct
- **Skip bad labels**: Continue printing good labels, report failures
- **Rollback**: Cancel job before printing starts

**Your Input Needed**: Which approach aligns with your quality control requirements?

---

### 11. Partial Print Recovery

**Question**: For a partial print (100 of 200 printed, then failure), what's the exact recovery process?

**Context**: This ties to question #3 about lot numbers.

**Specific Questions**:
1. Can operators manually verify which labels printed? (e.g., check box numbers)
2. Should the system display "last successful label" in the UI?
3. Is there a physical inspection step before retry?
4. Who is responsible for deciding whether to retry or reprint all?

**Your Input Needed**: Walk through the manual process for partial print recovery.

---

### 12. Retry Limits

**Question**: How many automatic retries before requiring manual intervention?

**Current Design**: 3 attempts per label with exponential backoff (1s, 2s, 4s)

**Scenarios**:
- **Transient error** (paper jam): Might succeed on retry 2
- **Persistent error** (printer offline): Will fail all 3 retries
- **Label-specific error** (invalid data): Will never succeed

**Your Input Needed**: 
1. Is 3 retries appropriate?
2. Should retry count differ by error type?
3. Who gets notified on final failure?

---

## Scale Integration Details

These questions clarify how weight data flows into the system.

### 13. Scale Connection

**Question**: How is the scale physically connected?

**Options**:
- **USB to Ubuntu box**: FastAPI could read directly
- **USB to different PC**: Must go through Odoo first
- **Network scale**: Could be read by either system
- **Serial connection**: Requires specific driver

**Your Input Needed**: 
1. What's the current scale setup?
2. Where does your Python scale script run?
3. Could FastAPI read from the scale directly, or must it go through Odoo?

---

### 14. Weight Data Timing

**Question**: When are catch weights determined relative to MO split?

**Scenario A: Weights Known Before Split**
```
1. Weigh all 200 boxes
2. Enter weights into Odoo (or Odoo reads from scale)
3. Split MO with weights already assigned
4. Submit print job with weights
```

**Scenario B: Weights Determined During Split**
```
1. Split MO into 200 units
2. Weigh each box as it's produced
3. Update weight in Odoo
4. Trigger label print
```

**Scenario C: Weights After Split**
```
1. Split MO into 200 units
2. Production completes
3. Weigh all boxes
4. Submit print job with weights
```

**Your Input Needed**: Which scenario matches your workflow?

---

### 15. Weight Data Storage

**Question**: Where is catch weight data currently stored in Odoo?

**Context**: We need to know which Odoo model/field to read from.

**Possibilities**:
- Custom field on `mrp.production`
- Custom field on `stock.move`
- Separate custom model
- Related to `stock.production.lot`

**Your Input Needed**: 
1. Which Odoo model stores catch weight?
2. Is it one weight per MO, or one per unit/lot?
3. Can you share the relevant Odoo model structure?

---

## Odoo Technical Capabilities

These questions help us understand Odoo SaaS limitations.

### 16. Database Access

**Question**: Can Odoo SaaS modules query PostgreSQL directly, or must they use the ORM?

**Context**: Direct SQL would allow more complex queries, but may not be available in SaaS.

**Your Input Needed**: 
1. Have you successfully run raw SQL in an Odoo.com module?
2. Are there any restrictions on database access?

---

### 17. Python Package Installation

**Question**: Can you install arbitrary Python packages in Odoo SaaS modules?

**Context**: We need packages like `requests`, `httpx`, potentially `pyjwt`.

**Specific Packages Needed**:
- `requests` or `httpx` (HTTP client)
- `pyjwt` (JWT validation)
- Any GS1 barcode libraries

**Your Input Needed**: 
1. Can you add dependencies to an Odoo.com module?
2. Are there any package restrictions?
3. Have you successfully imported external packages?

---

### 18. Cron Job Capabilities

**Question**: Can you create scheduled actions (cron jobs) in Odoo SaaS?

**Context**: We need a cron job that runs every 1 minute to poll job status.

**Your Input Needed**: 
1. Can you create cron jobs in Odoo.com?
2. What's the minimum frequency (1 minute? 5 minutes?)?
3. Are there any execution time limits?

---

## Operational Questions

These questions help us design for real-world usage.

### 19. Print Volume Projections

**Question**: What are your realistic print volume expectations?

**Context**: We designed for "potentially thousands per day" but need specifics.

**Specific Questions**:
1. Average labels per day?
2. Peak labels per day?
3. Average labels per batch?
4. Maximum labels per batch?
5. How many MO splits per day?
6. Busiest time of day/week?

**Your Input Needed**: Help us validate our capacity assumptions.

---

### 20. Manual Reprint Frequency

**Question**: How often do you expect to need manual reprints?

**Context**: We need to design the reprint UX appropriately.

**Scenarios**:
- Damaged labels (physical damage)
- Misprints (quality issues)
- Lost labels
- Wrong data printed

**Your Input Needed**: 
1. Estimated reprint frequency (X% of prints)?
2. Most common reprint reason?
3. Who typically triggers reprints (operators, QC, supervisors)?

---

### 21. Template Change Frequency

**Question**: How often do ZPL templates change?

**Context**: We designed templates as files on disk, not database records.

**Your Input Needed**: 
1. Expected template changes per month?
2. Who edits templates? (Just you, or multiple people?)
3. Do you need template approval workflow?

---

### 22. Downtime Tolerance

**Question**: What's the acceptable downtime for the print server?

**Context**: Helps us prioritize reliability features.

**Scenarios**:
- Planned maintenance (updates, config changes)
- Unplanned outages (crashes, network issues)
- Printer maintenance

**Your Input Needed**: 
1. Can printing be paused for 10 minutes? 1 hour? 4 hours?
2. Are there critical time windows (e.g., shipping deadlines)?
3. Do you need 24/7 operation?

---

## Future Expansion Questions

These questions help us design for future growth.

### 23. Multiple Printers

**Question**: Will you eventually have multiple printers?

**Context**: Affects database schema and API design.

**Scenarios**:
- Multiple printers in same location (load balancing)
- Printers in different locations (facility expansion)
- Different printer models (different label sizes)

**Your Input Needed**: 
1. Plans for additional printers in next 12 months?
2. Would they print the same labels, or different products?
3. Need for printer selection (manual or automatic)?

---

### 24. Multi-Location Support

**Question**: Will you have multiple commissaries/production facilities?

**Context**: Affects lot number sequence design.

**Considerations**:
- Lot numbers must be globally unique across all locations
- Each location might need its own print server
- Centralized monitoring vs. per-location

**Your Input Needed**: Expansion plans for additional locations?

---

### 25. Regulatory Compliance

**Question**: Are there any food safety regulations that affect label requirements?

**Context**: May require specific data retention, audit trails, or label formats.

**Potential Requirements**:
- FDA traceability requirements
- FSMA (Food Safety Modernization Act)
- State-specific regulations
- Customer/retailer requirements

**Your Input Needed**: 
1. Any compliance requirements we should design for?
2. Audit trail needs?
3. Data retention requirements?

---

## Summary by Priority

### Must Answer Before Development
1. Source of truth for lot numbers (Postgres vs. Odoo)
2. Lot number prerequisites (exist before or after printing)
3. Partial print failure handling
4. MO split mechanics

### Should Answer Before Development
5. Odoo webhook capability
6. GTIN validation requirements
7. Barcode format requirements
8. Scale connection details
9. Weight data timing

### Can Answer During Development
10. Additional GS1 AIs
11. Error handling preferences
12. Retry limits
13. Print volume projections
14. Operational preferences

### Nice to Know for Future
15. Multiple printer plans
16. Multi-location expansion
17. Regulatory compliance

---

## Response Template for Shun

Please copy this template and fill in your answers:

```markdown
# Shun's Responses to Open Questions

Date: [YYYY-MM-DD]

## Critical Path
1. Source of Truth: [Postgres / Odoo / Hybrid]
2. Lot Numbers Must Exist Before Printing: [Yes / No]
3. Partial Print Handling: [Your description]
4. Odoo Webhook Capability: [Yes / No]
5. MO Split Mechanics: [Your description]

## GS1 Barcode
6. GTIN Validation: [Required / Trust Odoo / Calculate]
7. Barcode Format: [Human / Machine / Both]
8. Additional AIs: [List or "None"]

## Error Handling
9. Printer Offline: [Queue / Timeout after X hours]
10. Invalid ZPL: [Fail job / Skip label]
11. Partial Print Recovery: [Your description]
12. Retry Limits: [3 is fine / Different number]

## Scale Integration
13. Scale Connection: [USB to Ubuntu / Other]
14. Weight Timing: [Before split / During / After]
15. Weight Storage: [Odoo model/field description]

## Odoo Technical
16. Database Access: [ORM only / Can use SQL]
17. Python Packages: [Can install / Restrictions]
18. Cron Jobs: [Can create / Frequency limits]

## Operational
19. Print Volume: [X labels/day average, Y peak]
20. Reprint Frequency: [X% of prints]
21. Template Changes: [X per month]
22. Downtime Tolerance: [X minutes acceptable]

## Future
23. Multiple Printers: [Plans / Timeline]
24. Multi-Location: [Plans / Timeline]
25. Compliance: [Requirements / None]
```

---

**Next Steps**: Once we receive Shun's responses, we can finalize the design and begin Phase 1 implementation.

**Document Status**: Awaiting Response  
**Last Updated**: 2025-10-02  
**Authors**: Joshua (questions), Claude (organization)