"""Batch Print Job Creation

Creates complete print jobs from MO split events, including lot number generation,
ZPL template population, and job record creation.

Source: F01-auto-print-on-mo-split.md - Example 4
"""

import json
from odoo import models, api


class LabelPrintJob(models.Model):
    _name = 'label.print.job'
    
    @api.model
    def create_from_mo_split(self, mo):
        """Create batch print job for MO split"""
        quantity = len(mo.move_raw_ids)  # Number of product units
        lot_numbers = self._generate_lot_numbers(mo.id, quantity)
        
        labels_data = []
        for idx, lot_number in enumerate(lot_numbers):
            label_zpl = self._generate_label_zpl(
                mo=mo,
                lot_number=lot_number,
                box_number=idx + 1,
                total_boxes=quantity
            )
            labels_data.append({
                'zpl_code': label_zpl,
                'lot_number': lot_number,
                'box_number': idx + 1
            })
        
        # Create print job record
        job = self.create({
            'mo_id': mo.id,
            'quantity': quantity,
            'status': 'pending',
            'labels_data': json.dumps(labels_data)
        })
        
        # Submit to Flask API
        job._submit_to_print_server()
        
        return job