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

> **Code Example**: See [appendix/code-examples/zpl/sample_template.zpl](../../../appendix/code-examples/zpl/sample_template.zpl)

A complete ZPL template demonstrating variable placeholders for product information, lot numbers, GS1 barcodes, and company details.

## Technical Implementation

### Data Model

> **Code Example**: See [appendix/code-examples/odoo/models/label_template.py](../../../appendix/code-examples/odoo/models/label_template.py)

The label template model supports versioning, assignment rules by product/category, and complete metadata tracking.

### Template Engine

> **Code Example**: See [appendix/code-examples/odoo/models/template_engine.py](../../../appendix/code-examples/odoo/models/template_engine.py)

The template engine handles variable substitution and intelligent template selection based on a three-tier priority system (specific product > category > default).

### Labelary Preview Integration

> **Code Example**: See [appendix/code-examples/odoo/models/labelary_preview.py](../../../appendix/code-examples/odoo/models/labelary_preview.py)

Generates label preview images using Labelary.com API with sample data, saving the PNG as an attachment for visual verification.

### Test Print

> **Code Example**: See [appendix/code-examples/odoo/models/test_print.py](../../../appendix/code-examples/odoo/models/test_print.py)

Sends a test label to the printer using sample data to verify template formatting and printer connectivity.

### Template Versioning

> **Code Example**: See [appendix/code-examples/odoo/models/template_versioning.py](../../../appendix/code-examples/odoo/models/template_versioning.py)

Automatically creates new versions when ZPL code is modified, maintaining history for audit and rollback purposes.

## User Interface

### Template List View

> **Code Example**: See [appendix/code-examples/odoo/views/template_list_view.xml](../../../appendix/code-examples/odoo/views/template_list_view.xml)

Tree view for label templates with quick action buttons for preview and test print.

### Template Form View (key fields)
- ZPL code editor with monospace font
- Variable reference guide (expandable panel)
- Preview button (generates PNG via Labelary)
- Test print button
- Assignment rules section
- Version history

## Validation

> **Code Example**: See [appendix/code-examples/odoo/models/zpl_validation.py](../../../appendix/code-examples/odoo/models/zpl_validation.py)

Basic ZPL syntax validation checks for matching ^XA/^XZ commands and proper structure.

## Related Documents
- [ZPL Templates Reference](../reference/zpl-templates.md)
- [Data Flows: Template Management](../architecture/data-flows.md#flow-3-template-management)