# Odoo Module Component

## Module Overview
Custom Odoo module that orchestrates label printing functionality, integrating with Odoo's MRP, inventory, and product modules.

## Module Structure

```
label_print/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── label_template.py
│   ├── print_job.py
│   ├── lot_number_generator.py
│   ├── gs1_barcode_generator.py
│   ├── mrp_production.py (inherit)
│   └── printer_configuration.py
├── views/
│   ├── label_template_views.xml
│   ├── print_job_views.xml
│   ├── mrp_production_views.xml
│   └── printer_configuration_views.xml
├── wizards/
│   ├── __init__.py
│   └── label_reprint_wizard.py
├── data/
│   ├── sequences.xml
│   └── default_templates.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── static/
│   ├── src/
│   │   └── js/
│   │       └── print_status_widget.js
│   └── description/
│       └── icon.png
└── README.md
```

## Manifest File

```python
# __manifest__.py
{
    'name': 'Label Print - Catch Weight',
    'version': '1.0.0',
    'category': 'Manufacturing',
    'summary': 'GS1-128 label printing for catch weight products',
    'description': """
        Automated label printing system for catch weight products
        with GS1-128 barcodes and Zebra Z230 printer integration.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'mrp',
        'stock',
        'product'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/default_templates.xml',
        'views/label_template_views.xml',
        'views/print_job_views.xml',
        'views/mrp_production_views.xml',
        'views/printer_configuration_views.xml',
        'wizards/label_reprint_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'label_print/static/src/js/print_status_widget.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
```

## Key Models

### label.template
- Stores ZPL templates with variable placeholders
- Assignment rules by product category
- Versioning support

### label.print.job
- Tracks all print jobs (auto and manual)
- Status lifecycle management
- Links to MO and lot numbers

### lot.number.generator
- Generates unique sequential lot numbers
- Links lot to MO, product, and catch weight
- Tracks print status per lot

### gs1.barcode.generator (Abstract)
- Generates GS1-128 compliant data strings
- Handles weight encoding
- Validates barcode format

### mrp.production (Inherited)
- Adds print/reprint buttons
- Detects MO split events
- Links to print jobs

### printer.configuration
- Stores printer details (name, IP, model)
- Status monitoring
- Default printer selection

## Security

### User Groups

```xml
<!-- security/security.xml -->
<odoo>
    <record id="group_label_print_user" model="res.groups">
        <field name="name">Label Print User</field>
        <field name="category_id" ref="base.module_category_manufacturing"/>
    </record>
    
    <record id="group_label_print_manager" model="res.groups">
        <field name="name">Label Print Manager</field>
        <field name="category_id" ref="base.module_category_manufacturing"/>
        <field name="implied_ids" eval="[(4, ref('group_label_print_user'))]"/>
    </record>
</odoo>
```

### Access Rights

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_label_template_user,label.template.user,model_label_template,group_label_print_user,1,0,0,0
access_label_template_manager,label.template.manager,model_label_template,group_label_print_manager,1,1,1,1
access_print_job_user,print.job.user,model_label_print_job,group_label_print_user,1,1,1,0
access_lot_generator_user,lot.generator.user,model_lot_number_generator,group_label_print_user,1,0,0,0
```

## Configuration

### System Parameters

```python
# Set via Settings → Technical → Parameters → System Parameters
KEY: label_print.api_url
VALUE: https://print-server.local:5000

KEY: label_print.api_key  
VALUE: your-secret-api-key-here

KEY: label_print.default_printer
VALUE: zebra_z230_line1
```

## Installation

1. Copy module to Odoo addons directory
2. Update apps list
3. Install "Label Print - Catch Weight" module
4. Configure system parameters
5. Create/import label templates
6. Configure printer(s)
7. Assign user groups

## Related Documents
- [System Architecture](../architecture/system-architecture.md)
- [Database Schema](../reference/database-schema.md)
- [Deployment Guide](../operations/deployment.md)