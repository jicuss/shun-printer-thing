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

```python
class PrintJobStatusPoller(models.AbstractModel):
    _name = 'print.job.status.poller'
    
    @api.model
    def poll_job_status(self, job_id):
        """Poll Flask server for job status"""
        job = self.env['label.print.job'].browse(job_id)
        
        if not job.flask_job_id or job.status in ['completed', 'failed', 'cancelled']:
            return
        
        # Call Flask API
        config = self.env['ir.config_parameter'].sudo()
        api_url = config.get_param('label_print.api_url')
        api_key = config.get_param('label_print.api_key')
        
        try:
            response = requests.get(
                f"{api_url}/api/status/{job.flask_job_id}",
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=5
            )
            response.raise_for_status()
            
            status_data = response.json()
            
            # Update job record
            job.write({
                'status': status_data.get('status'),
                'current_label': status_data.get('current_label', 0),
                'progress_percent': status_data.get('progress_percent', 0)
            })
            
            # If completed, send notification
            if status_data.get('status') == 'completed':
                self._send_completion_notification(job)
            
            # If failed, log error
            elif status_data.get('status') == 'failed':
                job.write({'error_message': status_data.get('error_message')})
                self._send_error_notification(job)
                
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to poll job status: {e}")
    
    def _send_completion_notification(self, job):
        """Send browser notification on job completion"""
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'label_print_notification',
            {
                'type': 'success',
                'title': 'Print Job Completed',
                'message': f"{job.quantity} labels printed for {job.mo_id.name}",
                'sticky': False
            }
        )
    
    def _send_error_notification(self, job):
        """Send browser notification on job failure"""
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'label_print_notification',
            {
                'type': 'danger',
                'title': 'Print Job Failed',
                'message': f"Job {job.id} failed: {job.error_message}",
                'sticky': True
            }
        )
```

### Scheduled Action (Cron)

```xml
<record id="cron_poll_print_job_status" model="ir.cron">
    <field name="name">Poll Print Job Status</field>
    <field name="model_id" ref="model_label_print_job"/>
    <field name="state">code</field>
    <field name="code">model._cron_poll_active_jobs()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">minutes</field>
    <field name="numbercall">-1</field>
    <field name="active" eval="True"/>
</record>
```

```python
@api.model
def _cron_poll_active_jobs(self):
    """Poll status for all active print jobs"""
    active_jobs = self.search([
        ('status', 'in', ['sent', 'queued', 'printing'])
    ])
    
    poller = self.env['print.job.status.poller']
    for job in active_jobs:
        poller.poll_job_status(job.id)
```

### Job Dashboard View

```python
class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    # Computed fields for dashboard
    progress_display = fields.Char(
        'Progress',
        compute='_compute_progress_display'
    )
    
    @api.depends('current_label', 'quantity')
    def _compute_progress_display(self):
        for job in self:
            if job.status == 'printing':
                job.progress_display = f"{job.current_label} of {job.quantity}"
            elif job.status == 'completed':
                job.progress_display = f"{job.quantity} of {job.quantity}"
            else:
                job.progress_display = "-"
```

### Dashboard Tree View

```xml
<tree string="Print Jobs" 
      decoration-success="status=='completed'"
      decoration-warning="status=='printing'"
      decoration-danger="status=='failed'"
      decoration-muted="status=='cancelled'">
    <field name="create_date" string="Submitted"/>
    <field name="mo_id"/>
    <field name="quantity"/>
    <field name="status"/>
    <field name="progress_display" string="Progress"/>
    <field name="job_type"/>
    <field name="submitted_by"/>
    
    <button name="action_retry" type="object" 
            string="Retry" icon="fa-repeat"
            attrs="{'invisible': [('status', '!=', 'failed')]}"/>
    
    <button name="action_cancel" type="object" 
            string="Cancel" icon="fa-times"
            attrs="{'invisible': [('status', 'not in', ['pending', 'sent', 'queued', 'printing'])]}"/>
</tree>
```

### Filtering & Search

```xml
<search>
    <field name="mo_id"/>
    <field name="submitted_by"/>
    
    <filter name="today" string="Today"
            domain="[('create_date', '&gt;=', context_today().strftime('%Y-%m-%d'))]"/>
    <filter name="this_week" string="This Week"
            domain="[('create_date', '&gt;=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]"/>
    
    <filter name="completed" string="Completed"
            domain="[('status', '=', 'completed')]"/>
    <filter name="failed" string="Failed"
            domain="[('status', '=', 'failed')]"/>
    <filter name="active" string="Active"
            domain="[('status', 'in', ['pending', 'sent', 'queued', 'printing'])]"/>
    
    <group expand="0" string="Group By">
        <filter name="group_status" string="Status" context="{'group_by': 'status'}"/>
        <filter name="group_mo" string="Manufacturing Order" context="{'group_by': 'mo_id'}"/>
        <filter name="group_date" string="Date" context="{'group_by': 'create_date:day'}"/>
    </group>
</search>
```

## Error Reporting

### Error Message Templates

```python
ERROR_MESSAGES = {
    'printer_offline': {
        'message': 'Printer is offline or not responding',
        'action': 'Check printer power and connection, then retry'
    },
    'network_timeout': {
        'message': 'Network connection to print server timed out',
        'action': 'Check network connection and retry'
    },
    'paper_out': {
        'message': 'Printer is out of paper or labels',
        'action': 'Load labels into printer and retry'
    },
    'invalid_zpl': {
        'message': 'Invalid ZPL code in template',
        'action': 'Contact administrator to fix template'
    }
}

def _format_error_message(self, error_code):
    """Format user-friendly error message"""
    if error_code in ERROR_MESSAGES:
        error_info = ERROR_MESSAGES[error_code]
        return f"{error_info['message']}. {error_info['action']}."
    return f"Unknown error: {error_code}"
```

## Export to CSV

```python
def action_export_history(self):
    """Export filtered print history to CSV"""
    jobs = self.search(self._context.get('active_domain', []))
    
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    
    # Header
    writer.writerow([
        'Date', 'MO Reference', 'Quantity', 'Status',
        'Job Type', 'Submitted By', 'Error Message'
    ])
    
    # Data
    for job in jobs:
        writer.writerow([
            job.create_date,
            job.mo_id.name if job.mo_id else '-',
            job.quantity,
            job.status,
            job.job_type,
            job.submitted_by.name,
            job.error_message or ''
        ])
    
    # Create attachment
    attachment = self.env['ir.attachment'].create({
        'name': f'print_history_{fields.Date.today()}.csv',
        'datas': base64.b64encode(csv_data.getvalue().encode('utf-8')),
        'mimetype': 'text/csv'
    })
    
    return {
        'type': 'ir.actions.act_url',
        'url': f'/web/content/{attachment.id}?download=true',
        'target': 'self'
    }
```

## Printer Status Widget

```xml
<record id="view_printer_status_kanban" model="ir.ui.view">
    <field name="name">printer.status.kanban</field>
    <field name="model">printer.configuration</field>
    <field name="arch" type="xml">
        <kanban>
            <field name="name"/>
            <field name="status"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_card">
                        <div class="o_kanban_card_content">
                            <div class="o_kanban_primary_left">
                                <div class="o_primary">
                                    <span><t t-esc="record.name.value"/></span>
                                </div>
                            </div>
                            <div class="o_kanban_primary_right">
                                <span t-if="record.status.raw_value == 'online'"
                                      class="badge badge-success">Online</span>
                                <span t-if="record.status.raw_value == 'offline'"
                                      class="badge badge-danger">Offline</span>
                            </div>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

## Related Documents
- [F01: Auto Print on MO Split](F01-auto-print-on-mo-split.md)
- [F04: Batch Print Queue](F04-batch-print-queue.md)
- [Flask API Component](../components/flask-api.md)