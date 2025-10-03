"""Reprint Job Creation

Creates print jobs for manual reprints, retrieving existing lot data and
generating labels for the specified boxes.

Source: F05-manual-reprint.md - Example 18
"""

import json
from odoo import models, api


class LabelPrintJob(models.Model):
    _inherit = 'label.print.job'
    
    @api.model
    def create_reprint_job(self, mo, lot_records, printer):
        """Create reprint job from existing lot records"""
        labels_data = []
        
        for lot in lot_records:
            zpl = self._generate_label_zpl(
                mo=mo,
                lot_number=lot.lot_number,
                box_number=lot.box_number,
                catch_weight=lot.catch_weight
            )
            labels_data.append({
                'zpl_code': zpl,
                'box_number': lot.box_number,
                'lot_number': lot.lot_number
            })
        
        job = self.create({
            'mo_id': mo.id,
            'quantity': len(labels_data),
            'labels_data': json.dumps(labels_data),
            'job_type': 'manual_reprint',
            'status': 'pending'
        })
        
        job._submit_to_print_server()
        return job