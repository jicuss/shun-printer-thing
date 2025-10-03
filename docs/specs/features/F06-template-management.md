# F06: Template Management

## Feature Overview
Provide administrators with tools to create, edit, and manage ZPL label templates with variable substitution, preview capabilities, and assignment rules.

## User Story
As a system administrator, I need to create and maintain label templates for different product categories so that labels can be customized for various packaging sizes and regulatory requirements.

## Acceptance Criteria
- [ ] CRUD operations for label templates (Create, Read, Update, Delete)
- [ ] ZPL code editor with syntax support
- [ ] Variable placeholder system (e.g., {PRODUCT_NAME}, {LOT_NUMBER})
- [ ] Template preview using Labelary.com API (300 DPI)
- [ ] Test print functionality to verify template on actual printer
- [ ] Template assignment rules by product category or SKU
- [ ] Template versioning to track changes
- [ ] Default template configuration

## Template Structure

### Variable Placeholders

| Variable | Description | Example Value |
|----------|-------------|---------------|
| {PRODUCT_NAME} | Product name | "Wild Caught Salmon" |
| {SKU} | Product SKU | "SALM-001" |
| {LOT_NUMBER} | Unique lot number | "LOT-2025-000001" |
| {WEIGHT} | Catch weight | "1.250" |
| {WEIGHT_UNIT} | Weight unit | "kg" |
| {GS1_BARCODE} | GS1-128 barcode data | (full data string) |
| {GS1_HUMAN_READABLE} | Human-readable GS1 | "(01)00012345..." |
| {PRODUCTION_DATE} | Production date | "2025-10-02" |
| {EXPIRATION_DATE} | Expiration date | "2025-11-02" |
| {MO_REFERENCE} | MO reference | "MO/2025/001" |
| {BOX_NUMBER} | Box number | "Box 1 of 200" |
| {COMPANY_NAME} | Company name | "ABC Commissary" |
| {COMPANY_ADDRESS} | Company address | "123 Main St" |

### Example ZPL Template

```zpl
^XA
^FO50,50^A0N,40,40^FD{PRODUCT_NAME}^FS
^FO50,100^A0N,30,30^FDSKU: {SKU}^FS
^FO50,140^A0N,25,25^FDLot: {LOT_NUMBER}^FS
^FO50,180^A0N,30,30^FDWeight: {WEIGHT} {WEIGHT_UNIT}^FS

^FO50,230^BY3,3,100^BC,100,Y,N,N
^FD{GS1_BARCODE}^FS

^FO50,350^A0N,20,20^FD{GS1_HUMAN_READABLE}^FS

^FO50,400^A0N,20,20^FDProduced: {PRODUCTION_DATE}^FS
^FO50,430^A0N,20,20^FD{BOX_NUMBER}^FS

^FO50,480^A0N,18,18^FD{COMPANY_NAME}^FS
^XZ
```

## Technical Implementation

### Data Model

```python
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
```

### Template Engine

```python
class LabelTemplateEngine(models.AbstractModel):
    _name = 'label.template.engine'
    
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
```

### Labelary Preview Integration

```python
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
```

### Test Print

```python
def action_test_print(self):
    """Send test label to printer"""
    self.ensure_one()
    
    # Use same sample data as preview
    sample_data = {...}  # Same as preview
    
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
```

### Template Versioning

```python
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
```

## User Interface

### Template List View
```xml
<tree string="Label Templates">
    <field name="name"/>
    <field name="code"/>
    <field name="version"/>
    <field name="is_default"/>
    <field name="active"/>
    <button name="action_preview_template" type="object" 
            icon="fa-eye" string="Preview"/>
    <button name="action_test_print" type="object" 
            icon="fa-print" string="Test Print"/>
</tree>
```

### Template Form View (key fields)
- ZPL code editor with monospace font
- Variable reference guide (expandable panel)
- Preview button (generates PNG via Labelary)
- Test print button
- Assignment rules section
- Version history

## Validation

```python
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
```

## Related Documents
- [ZPL Templates Reference](../reference/zpl-templates.md)
- [Data Flows: Template Management](../architecture/data-flows.md#flow-3-template-management)