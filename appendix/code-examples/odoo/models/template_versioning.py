"""Template Versioning

Automatically creates new versions when ZPL code is modified, maintaining
history for audit and rollback purposes.

Source: F06-template-management.md - Example 24
"""

from odoo import models, fields


class LabelTemplate(models.Model):
    _inherit = 'label.template'
    
    def write(self, vals):
        """Create new version when ZPL code changes"""
        if 'zpl_code' in vals and self.zpl_code != vals['zpl_code']:
            # Create copy of current version
            old_version = self.copy({
                'name': f"{self.name} (v{self.version})",
                'code': f"{self.code}_v{self.version}",
                'active': False,
                'version': self.version
            })
            
            vals['version'] = self.version + 1
            vals['previous_version_id'] = old_version.id
            vals['modified_by'] = self.env.user.id
            vals['modified_date'] = fields.Datetime.now()
        
        return super().write(vals)