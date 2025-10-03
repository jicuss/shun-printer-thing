"""ZPL Syntax Validation

Basic validation of ZPL code structure to catch common syntax errors
before templates are used in production.

Source: F06-template-management.md - Example 26
"""

from odoo import models, api
from odoo.exceptions import ValidationError


class LabelTemplate(models.Model):
    _inherit = 'label.template'
    
    @api.constrains('zpl_code')
    def _check_zpl_syntax(self):
        """Basic ZPL syntax validation"""
        for template in self:
            zpl = template.zpl_code
            
            # Check for matching ^XA and ^XZ
            if zpl.count('^XA') != zpl.count('^XZ'):
                raise ValidationError("Mismatched ^XA and ^XZ commands")
            
            # Check for required structure
            if not zpl.strip().startswith('^XA'):
                raise ValidationError("ZPL must start with ^XA")
            
            if not zpl.strip().endswith('^XZ'):
                raise ValidationError("ZPL must end with ^XZ")