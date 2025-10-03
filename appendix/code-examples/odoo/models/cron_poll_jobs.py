"""Cron Job for Polling Active Jobs

Scheduled method that finds all active print jobs and polls their status.

Source: F07-job-monitoring.md - Example 29
"""

from odoo import models, api


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    @api.model
    def _cron_poll_active_jobs(self):
        """Poll status for all active print jobs"""
        active_jobs = self.search([
            ('status', 'in', ['sent', 'queued', 'printing'])
        ])
        
        poller = self.env['print.job.status.poller']
        for job in active_jobs:
            poller.poll_job_status(job.id)