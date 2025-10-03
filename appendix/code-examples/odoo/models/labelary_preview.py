"""Labelary Preview Integration

Generates label preview images using the Labelary.com API for template validation
and visual verification before printing.

Source: F06-template-management.md - Example 22
"""

import base64
import requests
from odoo import models
from odoo.exceptions import UserError


class LabelTemplate(models.Model):
    _inherit = 'label.template'
    
    def action_preview_template(self):
        """Generate preview using Labelary.com API"""
        self.ensure_one()
        
        # Sample data for preview
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
        
        # Render template
        zpl = self.env['label.template.engine'].render_template(self, sample_data)
        
        # Call Labelary API
        url = f"http://api.labelary.com/v1/printers/{self.dpi}dpmm/labels/{self.width}x{self.height}/0/"
        
        try:
            response = requests.post(
                url,
                data=zpl.encode('utf-8'),
                headers={'Accept': 'image/png'},
                timeout=10
            )
            response.raise_for_status()
            
            # Save preview image as attachment
            attachment = self.env['ir.attachment'].create({
                'name': f'{self.name}_preview.png',
                'type': 'binary',
                'datas': base64.b64encode(response.content),
                'res_model': self._name,
                'res_id': self.id,
                'mimetype': 'image/png'
            })
            
            # Return action to display image
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/image/{attachment.id}',
                'target': 'new'
            }
            
        except requests.exceptions.RequestException as e:
            raise UserError(f"Failed to generate preview: {str(e)}")