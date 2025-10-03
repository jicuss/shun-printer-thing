# F05: Manual Reprint

## Feature Overview
Allow commissary staff to manually reprint labels for specific boxes, ranges, or entire manufacturing orders through an intuitive user interface.

## User Story
As a commissary operator, when labels are damaged, misprinted, or lost, I want to quickly reprint specific labels without reprinting the entire batch so that I can minimize waste and downtime.

## Acceptance Criteria
- [ ] Reprint button accessible from Manufacturing Order view
- [ ] Option to reprint all labels for an MO
- [ ] Option to reprint a range of boxes (e.g., boxes 45-50)
- [ ] Option to reprint a single box by number
- [ ] Reprinted labels contain same data as original
- [ ] Reprint action logged in job history
- [ ] Interface is touch-friendly for shop floor tablets

## User Interface

### MO Form View
```
┌────────────────────────────────┐
│ MO: MO/2025/001                │
│ Product: Catch Weight Seafood  │
│ Quantity: 200 boxes            │
│                                │
│ [🖨️ Reprint Labels] [History]  │
└────────────────────────────────┘
```

### Reprint Dialog
```
┌─────────────────────────────────┐
│ Reprint Labels - MO/2025/001    │
│                                 │
│ ◉ Reprint All (200 labels)      │
│ ○ Reprint Range                 │
│    From: [__] To: [__]          │
│ ○ Reprint Single Box            │
│    Box Number: [__]             │
│                                 │
│ Printer: [Zebra Z230 ▼]         │
│                                 │
│ [Cancel]      [Print Selected]  │
└─────────────────────────────────┘
```

## Technical Implementation

### Reprint Wizard

> **Code Example**: See [appendix/code-examples/odoo/wizards/label_reprint_wizard.py](../../../appendix/code-examples/odoo/wizards/label_reprint_wizard.py)

Transient model wizard providing a user-friendly interface for reprinting labels with three modes: all, range, or single box.

### Job Creation

> **Code Example**: See [appendix/code-examples/odoo/models/reprint_job_creation.py](../../../appendix/code-examples/odoo/models/reprint_job_creation.py)

Creates print jobs for manual reprints by retrieving existing lot data and regenerating ZPL for the selected boxes.

## Audit Trail
- Log all reprint actions with user, timestamp, and box numbers
- Track reprint reason (optional field)
- Maintain history for compliance audits

## Related Documents
- [F01: Auto Print](F01-auto-print-on-mo-split.md)
- [Data Flows](../architecture/data-flows.md#flow-2-manual-reprint)