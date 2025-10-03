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

```python
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def action_split_production(self):
        """Override split action to trigger label printing"""
        result = super().action_split_production()
        
        # Trigger automatic label generation
        if self.env.context.get('auto_print_labels', True):
            self._trigger_label_printing()
        
        return result
    
    def _trigger_label_printing(self):
        """Initiate automatic label print workflow"""
        LabelPrintJob = self.env['label.print.job']
        LabelPrintJob.create_from_mo_split(self)
```

### 2. Event Listener Registration

**Alternative**: Use Odoo automation rules (no-code approach)
- Trigger: "Manufacturing Order" record is updated
- Condition: State changed to specific split-complete status
- Action: Execute Python code to initiate label printing

### 3. Lot Number Generation

**Logic**:
```python
def _generate_lot_numbers(self, mo_id, quantity):
    """Generate sequential lot numbers for MO split"""
    year = fields.Date.today().year
    base_sequence = self.env['ir.sequence'].next_by_code('lot.number.sequence')
    
    lot_numbers = []
    for i in range(quantity):
        lot_number = f"LOT-{year}-{base_sequence + i:06d}"
        lot_numbers.append(lot_number)
    
    return lot_numbers
```

### 4. Label Data Preparation

**For each product unit**:
- Retrieve product master data (name, SKU, GTIN)
- Fetch catch weight from catch weight module
- Get production/expiration dates
- Generate GS1-128 barcode data string
- Populate ZPL template with all variables

### 5. Batch Print Job Creation

```python
def create_from_mo_split(self, mo):
    """Create batch print job for MO split"""
    quantity = len(mo.move_raw_ids)  # Number of product units
    lot_numbers = self._generate_lot_numbers(mo.id, quantity)
    
    labels_data = []
    for idx, lot_number in enumerate(lot_numbers):
        label_zpl = self._generate_label_zpl(
            mo=mo,
            lot_number=lot_number,
            box_number=idx + 1,
            total_boxes=quantity
        )
        labels_data.append({
            'zpl_code': label_zpl,
            'lot_number': lot_number,
            'box_number': idx + 1
        })
    
    # Create print job record
    job = self.create({
        'mo_id': mo.id,
        'quantity': quantity,
        'status': 'pending',
        'labels_data': json.dumps(labels_data)
    })
    
    # Submit to Flask API
    job._submit_to_print_server()
    
    return job
```

### 6. API Submission

```python
def _submit_to_print_server(self):
    """Send print job to Flask server"""
    config = self.env['ir.config_parameter'].sudo()
    api_url = config.get_param('label_print.api_url')
    api_key = config.get_param('label_print.api_key')
    printer_name = config.get_param('label_print.default_printer')
    
    payload = {
        'printer': printer_name,
        'quantity': self.quantity,
        'labels': json.loads(self.labels_data),
        'job_metadata': {
            'mo_reference': self.mo_id.name,
            'priority': 'normal'
        }
    }
    
    try:
        response = requests.post(
            f"{api_url}/api/print",
            json=payload,
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        self.write({
            'flask_job_id': result['job_id'],
            'status': 'sent'
        })
        
        # Start polling for status
        self._start_status_polling()
        
    except requests.exceptions.RequestException as e:
        self.write({
            'status': 'failed',
            'error_message': str(e)
        })
        self._handle_print_failure()
```

### 7. Status Polling

```python
def _start_status_polling(self):
    """Begin polling Flask server for job status"""
    # Schedule cron job or use @api.model scheduled action
    self.env.ref('label_print.poll_print_status_cron').sudo().write({
        'active': True,
        'nextcall': fields.Datetime.now()
    })
```

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
```python
class LabelPrintJob(models.Model):
    _name = 'label.print.job'
    _description = 'Label Print Job'
    
    mo_id = fields.Many2one('mrp.production', required=True)
    flask_job_id = fields.Char('External Job ID')
    quantity = fields.Integer('Label Quantity', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('sent', 'Sent to Printer'),
        ('printing', 'Printing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    labels_data = fields.Text('Label Data (JSON)')  # Store ZPL codes
    error_message = fields.Text('Error Message')
    submitted_date = fields.Datetime('Submitted At', default=fields.Datetime.now)
    completed_date = fields.Datetime('Completed At')
```

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