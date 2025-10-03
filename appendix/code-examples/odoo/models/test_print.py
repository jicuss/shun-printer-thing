"""Test Print Functionality

Sends a test label to the printer using sample data to verify template
formatting and printer connectivity.

Source: F06-template-management.md - Example 23
"""

import json
from odoo import models


class LabelTemplate(models.Model):
    _inherit = 'label.template'
    
    def action_test_print(self):
        """Send test label to printer"""
        self.ensure_one()
        
        # Use same sample data as preview
        sample_data = {
            'PRODUCT_NAME': 'Sample Product',
            'SKU': 'SAMPLE-001',
            'LOT_NUMBER': 'LOT-2025-000001',
            'WEIGHT': '1.250',
            'WEIGHT_UNIT': 'kg',
            'GS1_BARCODE': '>800012345678905>8LOT2025000001',
            'GS1_HUMAN_READABLE': '(01)00012345678905(10)LOT-2025-000001',
            'PRODUCTION_DATE': '2025-10-02',
            'EXPIRATION_DATE': '2025-11-02',
            'MO_REFERENCE': 'MO/2025/001',
            'BOX_NUMBER': 'Box 1 of 200',
            'COMPANY_NAME': 'Sample Company',
            'COMPANY_ADDRESS': '123 Main Street'
        }
        
        zpl = self.env['label.template.engine'].render_template(self, sample_data)
        
        # Create test print job
        job = self.env['label.print.job'].create({
            'mo_id': False,  # No MO for test print
            'quantity': 1,
            'status': 'pending',
            'labels_data': json.dumps([{'zpl_code': zpl}]),
            'job_type': 'test_print'
        })
        
        job._submit_to_print_server()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Test Print Sent',
                'message': 'Test label sent to printer',
                'type': 'info'
            }
        }