"""Label Template Model

Manages ZPL label templates with versioning, assignment rules, and metadata.
Supports variable placeholders for dynamic content population.

Source: F06-template-management.md - Example 20
"""

from odoo import models, fields, api


class LabelTemplate(models.Model):
    _name = 'label.template'
    _description = 'Label Template'
    
    name = fields.Char('Template Name', required=True)
    code = fields.Char('Template Code', required=True, index=True)
    zpl_code = fields.Text('ZPL Code', required=True)
    dpi = fields.Integer('DPI', default=300, required=True)
    width = fields.Float('Width (inches)', default=4.0)
    height = fields.Float('Height (inches)', default=6.0)
    
    active = fields.Boolean('Active', default=True)
    is_default = fields.Boolean('Default Template', default=False)
    
    # Assignment rules
    product_categ_ids = fields.Many2many(
        'product.category',
        string='Product Categories'
    )
    product_ids = fields.Many2many(
        'product.product',
        string='Specific Products'
    )
    
    # Versioning
    version = fields.Integer('Version', default=1, readonly=True)
    previous_version_id = fields.Many2one(
        'label.template',
        'Previous Version',
        readonly=True
    )
    
    # Metadata
    notes = fields.Text('Notes')
    created_by = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now, readonly=True)
    modified_by = fields.Many2one('res.users', 'Modified By')
    modified_date = fields.Datetime('Modified Date', readonly=True)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Template code must be unique!')
    ]