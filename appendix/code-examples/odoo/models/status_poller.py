"""Print Job Status Polling Service

Periodically polls the Flask server for job status updates and sends browser
notifications for completion or errors.

Source: F07-job-monitoring.md - Example 27
"""

import requests
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class PrintJobStatusPoller(models.AbstractModel):
    _name = 'print.job.status.poller'
    _description = 'Print Job Status Poller'
    
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