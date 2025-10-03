"""Template Engine

Handles ZPL template rendering with variable substitution and template selection
based on product assignment rules.

Source: F06-template-management.md - Example 21
"""

import re
import logging
from odoo import models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class LabelTemplateEngine(models.AbstractModel):
    _name = 'label.template.engine'
    _description = 'Label Template Engine'
    
    @api.model
    def render_template(self, template, data):
        """Render ZPL template with variable substitution"""
        zpl = template.zpl_code
        
        # Replace all variables
        for key, value in data.items():
            placeholder = '{' + key + '}'
            zpl = zpl.replace(placeholder, str(value or ''))
        
        # Check for unreplaced variables
        unreplaced = re.findall(r'\{[A-Z_]+\}', zpl)
        if unreplaced:
            _logger.warning(f"Unreplaced variables in template: {unreplaced}")
        
        return zpl
    
    @api.model
    def get_template_for_product(self, product):
        """Find appropriate template for product"""
        # Priority 1: Specific product assignment
        template = self.env['label.template'].search([
            ('product_ids', 'in', product.id),
            ('active', '=', True)
        ], limit=1)
        
        if template:
            return template
        
        # Priority 2: Product category assignment
        template = self.env['label.template'].search([
            ('product_categ_ids', 'in', product.categ_id.id),
            ('active', '=', True)
        ], limit=1)
        
        if template:
            return template
        
        # Priority 3: Default template
        template = self.env['label.template'].search([
            ('is_default', '=', True),
            ('active', '=', True)
        ], limit=1)
        
        if not template:
            raise ValidationError(
                f"No template found for product {product.display_name}"
            )
        
        return template