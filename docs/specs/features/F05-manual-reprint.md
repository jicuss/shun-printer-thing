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
```python
class LabelReprintWizard(models.TransientModel):
    _name = 'label.reprint.wizard'
    
    mo_id = fields.Many2one('mrp.production', required=True)
    reprint_type = fields.Selection([
        ('all', 'Reprint All'),
        ('range', 'Reprint Range'),
        ('single', 'Reprint Single Box')
    ], default='all')
    
    from_box = fields.Integer('From Box', default=1)
    to_box = fields.Integer('To Box')
    single_box = fields.Integer('Box Number')
    printer_id = fields.Many2one('printer.configuration')
    
    def action_reprint(self):
        # Determine boxes to reprint
        if self.reprint_type == 'all':
            box_numbers = range(1, self.to_box + 1)
        elif self.reprint_type == 'range':
            box_numbers = range(self.from_box, self.to_box + 1)
        else:
            box_numbers = [self.single_box]
        
        # Retrieve lot data
        lot_records = self.env['lot.number.generator'].search([
            ('mo_id', '=', self.mo_id.id),
            ('box_number', 'in', list(box_numbers))
        ])
        
        # Create reprint job
        return self.env['label.print.job'].create_reprint_job(
            mo=self.mo_id,
            lot_records=lot_records,
            printer=self.printer_id
        )
```

### Job Creation
```python
@api.model
def create_reprint_job(self, mo, lot_records, printer):
    labels_data = []
    for lot in lot_records:
        zpl = self._generate_label_zpl(
            mo=mo,
            lot_number=lot.lot_number,
            box_number=lot.box_number,
            catch_weight=lot.catch_weight
        )
        labels_data.append({'zpl_code': zpl, 'box_number': lot.box_number})
    
    job = self.create({
        'mo_id': mo.id,
        'quantity': len(labels_data),
        'labels_data': json.dumps(labels_data),
        'job_type': 'manual_reprint'
    })
    
    job._submit_to_print_server()
    return job
```

## Audit Trail
- Log all reprint actions with user, timestamp, and box numbers
- Track reprint reason (optional field)
- Maintain history for compliance audits

## Related Documents
- [F01: Auto Print](F01-auto-print-on-mo-split.md)
- [Data Flows](../architecture/data-flows.md#flow-2-manual-reprint)