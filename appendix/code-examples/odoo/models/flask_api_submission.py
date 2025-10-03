"""Flask API Submission

Handles submission of print jobs to the Flask print server with error handling
and status polling initiation.

Source: F01-auto-print-on-mo-split.md - Example 5
"""

import json
import requests
from odoo import models, fields


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
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