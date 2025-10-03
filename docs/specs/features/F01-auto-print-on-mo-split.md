# F01: Automatic Print on MO Split

## Feature Overview
Automatically detect Manufacturing Order (MO) split events and trigger batch label printing without user intervention.

## User Story
As a commissary operator, when I split a Manufacturing Order into multiple product units (e.g., 200 boxes), I want labels to automatically print for all units so that I don't have to manually initiate printing and can focus on production tasks.

## Acceptance Criteria
- [ ] System detects MO split event within 1 second of completion
- [ ] Unique lot numbers are generated for each product unit
- [ ] Print job is automatically created and submitted to Flask server
- [ ] All labels print successfully (>95% success rate)
- [ ] No user interaction required for standard print flow
- [ ] User receives visual confirmation when printing completes
- [ ] Failed jobs are logged with clear error messages

## Technical Implementation

### 1. MO Split Detection

**Approach**: Odoo workflow hook/override

> **Code Example**: See [appendix/code-examples/odoo/models/mrp_production_split.py](../../../appendix/code-examples/odoo/models/mrp_production_split.py)

The MRP Production model is extended to override the `action_split_production` method, automatically triggering label printing when a manufacturing order is split into multiple units.

### 2. Event Listener Registration

**Alternative**: Use Odoo automation rules (no-code approach)
- Trigger: "Manufacturing Order" record is updated
- Condition: State changed to specific split-complete status
- Action: Execute Python code to initiate label printing

### 3. Lot Number Generation

> **Code Example**: See [appendix/code-examples/odoo/models/lot_number_generation.py](../../../appendix/code-examples/odoo/models/lot_number_generation.py)

**Logic**: Sequential lot numbers are generated using Odoo's ir.sequence with year-based prefixes (e.g., LOT-2025-000001).

### 4. Label Data Preparation

**For each product unit**:
- Retrieve product master data (name, SKU, GTIN)
- Fetch catch weight from catch weight module
- Get production/expiration dates
- Generate GS1-128 barcode data string
- Populate ZPL template with all variables

### 5. Batch Print Job Creation

> **Code Example**: See [appendix/code-examples/odoo/models/print_job_creation.py](../../../appendix/code-examples/odoo/models/print_job_creation.py)

The `create_from_mo_split` method orchestrates the entire print job creation process: generating lot numbers, populating ZPL templates, creating the job record, and submitting to the Flask API.

### 6. API Submission

> **Code Example**: See [appendix/code-examples/odoo/models/flask_api_submission.py](../../../appendix/code-examples/odoo/models/flask_api_submission.py)

Submits the print job to the Flask server via HTTP POST with authentication, error handling, and automatic status polling initiation.

### 7. Status Polling

> **Code Example**: See [appendix/code-examples/odoo/models/status_polling.py](../../../appendix/code-examples/odoo/models/status_polling.py)

Initiates periodic polling of the Flask server to track print job progress and completion status.

### 8. User Notification

**On Success**:
- Display toast notification: "✓ 200 labels printed successfully for MO/2025/001"
- Update MO form view with print status badge

**On Failure**:
- Display error notification with actionable message
- Provide "Retry" button
- Log error details for troubleshooting

## Data Model

### label.print.job

> **Code Example**: See [appendix/code-examples/odoo/models/label_print_job.py](../../../appendix/code-examples/odoo/models/label_print_job.py)

The print job model tracks all label printing operations with status lifecycle, error logging, and links to manufacturing orders.

## Error Handling

### Printer Offline
- Detect via Flask API error response
- Mark job as failed with clear message
- Notify user: "Printer is offline. Please check printer and retry."

### Network Timeout
- Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- If all retries fail, mark as failed and notify user

### Partial Print (e.g., jammed after 50 labels)
- Flask tracks progress
- On resume, skip already-printed labels
- Continue from label 51

## Performance Requirements
- MO split detection latency: <1 second
- Lot number generation (200 units): <2 seconds
- Label data preparation (200 units): <3 seconds
- Total time from split to first label printing: <10 seconds

## Related Documents
- [Data Flows: Automated Print](../architecture/data-flows.md#flow-1-automated-print-on-mo-split)
- [F02: Lot Number Generation](F02-lot-number-generation.md)
- [F03: GS1 Barcode Creation](F03-gs1-barcode-creation.md)