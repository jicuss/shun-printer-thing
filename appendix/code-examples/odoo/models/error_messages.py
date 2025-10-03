"""Error Message Templates

Predefined error messages with actionable troubleshooting steps.

Source: F07-job-monitoring.md - Example 33
"""

from odoo import models


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


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    def _format_error_message(self, error_code):
        """Format user-friendly error message"""
        if error_code in ERROR_MESSAGES:
            error_info = ERROR_MESSAGES[error_code]
            return f"{error_info['message']}. {error_info['action']}."
        return f"Unknown error: {error_code}"