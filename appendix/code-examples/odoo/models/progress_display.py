"""Progress Display Computed Field

Computed field that formats progress information for display in the UI.

Source: F07-job-monitoring.md - Example 30
"""

from odoo import models, fields, api


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    # Add fields for progress tracking
    current_label = fields.Integer('Current Label', default=0)
    progress_percent = fields.Float('Progress %', default=0.0)
    
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