"""Status Polling Initialization

Initiates periodic status polling for print jobs after submission to Flask server.

Source: F01-auto-print-on-mo-split.md - Example 6
"""

from odoo import models, fields


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    def _start_status_polling(self):
        """Begin polling Flask server for job status"""
        # Schedule cron job or use @api.model scheduled action
        self.env.ref('label_print.poll_print_status_cron').sudo().write({
            'active': True,
            'nextcall': fields.Datetime.now()
        })