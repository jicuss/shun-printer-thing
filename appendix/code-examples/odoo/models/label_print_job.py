"""Label Print Job Data Model

Complete data model definition for tracking print jobs throughout their lifecycle.

Source: F01-auto-print-on-mo-split.md - Example 7
"""

from odoo import models, fields


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