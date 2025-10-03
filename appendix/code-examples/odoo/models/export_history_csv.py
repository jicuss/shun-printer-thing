"""Export Print History to CSV

Exports filtered print job history to CSV format for reporting and analysis.

Source: F07-job-monitoring.md - Example 34
"""

import io
import csv
import base64
from odoo import models, fields


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    def action_export_history(self):
        """Export filtered print history to CSV"""
        jobs = self.search(self._context.get('active_domain', []))
        
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        
        # Header
        writer.writerow([
            'Date', 'MO Reference', 'Quantity', 'Status',
            'Job Type', 'Submitted By', 'Error Message'
        ])
        
        # Data
        for job in jobs:
            writer.writerow([
                job.create_date,
                job.mo_id.name if job.mo_id else '-',
                job.quantity,
                job.status,
                job.job_type,
                job.submitted_by.name,
                job.error_message or ''
            ])
        
        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'print_history_{fields.Date.today()}.csv',
            'datas': base64.b64encode(csv_data.getvalue().encode('utf-8')),
            'mimetype': 'text/csv'
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self'
        }