"""Label Reprint Wizard

Transient model wizard that provides UI for manual label reprinting with options
for all labels, a range, or a single box.

Source: F05-manual-reprint.md - Example 17
"""

from odoo import models, fields, api


class LabelReprintWizard(models.TransientModel):
    _name = 'label.reprint.wizard'
    _description = 'Label Reprint Wizard'
    
    mo_id = fields.Many2one('mrp.production', required=True)
    reprint_type = fields.Selection([
        ('all', 'Reprint All'),
        ('range', 'Reprint Range'),
        ('single', 'Reprint Single Box')
    ], default='all', required=True)
    
    from_box = fields.Integer('From Box', default=1)
    to_box = fields.Integer('To Box')
    single_box = fields.Integer('Box Number')
    printer_id = fields.Many2one('printer.configuration', 'Printer')
    
    @api.onchange('mo_id')
    def _onchange_mo_id(self):
        """Set default to_box based on MO quantity"""
        if self.mo_id:
            self.to_box = len(self.mo_id.move_raw_ids)
    
    def action_reprint(self):
        """Execute reprint based on selected options"""
        self.ensure_one()
        
        # Determine boxes to reprint
        if self.reprint_type == 'all':
            box_numbers = range(1, self.to_box + 1)
        elif self.reprint_type == 'range':
            box_numbers = range(self.from_box, self.to_box + 1)
        else:  # single
            box_numbers = [self.single_box]
        
        # Retrieve lot data
        lot_records = self.env['lot.number.generator'].search([
            ('mo_id', '=', self.mo_id.id),
            ('box_number', 'in', list(box_numbers))
        ])
        
        if not lot_records:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Labels Found',
                    'message': 'No labels found for the specified range.',
                    'type': 'warning'
                }
            }
        
        # Create reprint job
        job = self.env['label.print.job'].create_reprint_job(
            mo=self.mo_id,
            lot_records=lot_records,
            printer=self.printer_id
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Reprint Submitted',
                'message': f'Reprint job for {len(lot_records)} labels has been submitted.',
                'type': 'success'
            }
        }