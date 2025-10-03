# F07: Job Monitoring & History

## Feature Overview
Provide real-time monitoring of print jobs with status tracking, history dashboard, error reporting, and user notifications.

## User Story
As a production supervisor, I need to monitor the status of print jobs and review print history so that I can ensure all labels are printed correctly and troubleshoot any issues quickly.

## Acceptance Criteria
- [ ] Real-time job status updates (queued, printing, completed, failed)
- [ ] Progress indicator for batch jobs (e.g., "150 of 200 printed")
- [ ] Print job history with filtering and search
- [ ] Error messages with actionable troubleshooting steps
- [ ] Visual notifications (toast messages) for job completion
- [ ] Export print history to CSV for reporting
- [ ] Printer status monitoring (online/offline)

## Job Status Lifecycle

```
Pending → Sent → Printing → Completed
                    ↓
                 Failed → Retry
```

### Status Definitions

| Status | Description | User Action |
|--------|-------------|-------------|
| **Pending** | Job created, awaiting submission | Wait |
| **Sent** | Submitted to Flask server | Wait |
| **Queued** | In Flask print queue | Wait |
| **Printing** | Currently printing labels | Monitor progress |
| **Completed** | All labels printed successfully | None |
| **Completed with Errors** | Printed with some failures | Review failed labels |
| **Failed** | Job failed completely | Retry or check printer |
| **Cancelled** | User cancelled job | None |

## Technical Implementation

### Status Polling Service

> **Code Example**: See [appendix/code-examples/odoo/models/status_poller.py](../../../appendix/code-examples/odoo/models/status_poller.py)

Periodically polls Flask server for job status updates and sends browser notifications for completion or errors.

### Scheduled Action (Cron)

> **Code Examples**: 
> - XML: [appendix/code-examples/odoo/data/status_polling_cron.xml](../../../appendix/code-examples/odoo/data/status_polling_cron.xml)
> - Python: [appendix/code-examples/odoo/models/cron_poll_jobs.py](../../../appendix/code-examples/odoo/models/cron_poll_jobs.py)

Cron job that runs every minute to poll status for all active print jobs.

### Job Dashboard View

> **Code Example**: See [appendix/code-examples/odoo/models/progress_display.py](../../../appendix/code-examples/odoo/models/progress_display.py)

Computed field that formats progress information for display in the UI.

### Dashboard Tree View

> **Code Example**: See [appendix/code-examples/odoo/views/job_dashboard_tree.xml](../../../appendix/code-examples/odoo/views/job_dashboard_tree.xml)

Tree view with status-based color decorations and action buttons for retry and cancel.

### Filtering & Search

> **Code Example**: See [appendix/code-examples/odoo/views/job_search_filters.xml](../../../appendix/code-examples/odoo/views/job_search_filters.xml)

Search view with filters for status, date ranges, and grouping options.

## Error Reporting

### Error Message Templates

> **Code Example**: See [appendix/code-examples/odoo/models/error_messages.py](../../../appendix/code-examples/odoo/models/error_messages.py)

Predefined error messages with actionable troubleshooting steps for common printer issues.

## Export to CSV

> **Code Example**: See [appendix/code-examples/odoo/models/export_history_csv.py](../../../appendix/code-examples/odoo/models/export_history_csv.py)

Exports filtered print job history to CSV format for reporting and analysis.

## Printer Status Widget

> **Code Example**: See [appendix/code-examples/odoo/views/printer_status_kanban.xml](../../../appendix/code-examples/odoo/views/printer_status_kanban.xml)

Kanban view for monitoring printer status and availability with visual online/offline indicators.

## Related Documents
- [F01: Auto Print on MO Split](F01-auto-print-on-mo-split.md)
- [F04: Batch Print Queue](F04-batch-print-queue.md)
- [Flask API Component](../components/flask-api.md)