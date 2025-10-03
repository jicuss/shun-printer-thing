# F02: Lot Number Generation

## Feature Overview
Generate unique, sequential lot numbers for each product unit created during an MO split, ensuring traceability and compliance with food safety regulations.

## User Story
As a quality control manager, I need each product unit to have a unique lot number so that I can trace products throughout the supply chain and quickly identify affected units in case of recalls.

## Acceptance Criteria
- [ ] Each product unit receives a unique lot number
- [ ] Lot numbers follow a consistent, configurable format
- [ ] No duplicate lot numbers are generated
- [ ] Lot numbers are sequential within a production date
- [ ] System prevents lot number collisions even with concurrent MO splits
- [ ] Lot numbers are stored and linked to MO, product, and catch weight data
- [ ] Historical lot numbers are preserved for audit trail

## Lot Number Format

### Standard Format
```
LOT-{YEAR}-{SEQUENCE}
```

**Examples**:
- `LOT-2025-000001`
- `LOT-2025-000002`
- `LOT-2025-012345`

### Components
- **Prefix**: `LOT-` (configurable)
- **Year**: 4-digit year (e.g., 2025)
- **Sequence**: 6-digit zero-padded sequential number

### Alternative Formats (Configurable)
```
{PREFIX}-{YEAR}{MONTH}{DAY}-{SEQUENCE}
# Example: LOT-20251002-001

{PREFIX}-{PRODUCT_CODE}-{YEAR}-{SEQUENCE}
# Example: LOT-SALM-2025-001

{FACILITY_CODE}-{YEAR}{JULIAN_DAY}-{SEQUENCE}
# Example: FAC1-2025275-001
```

## Technical Implementation

### 1. Sequence Configuration

**Odoo Sequence Definition** (`data/sequences.xml`):
```xml
<odoo>
    <data noupdate="1">
        <record id="seq_lot_number" model="ir.sequence">
            <field name="name">Lot Number Sequence</field>
            <field name="code">lot.number.sequence</field>
            <field name="prefix">LOT-%(year)s-</field>
            <field name="padding">6</field>
            <field name="number_increment">1</field>
            <field name="implementation">standard</field>
            <field name="use_date_range">True</field>
        </record>
    </data>
</odoo>
```

### 2. Generation Logic

```python
class LotNumberGenerator(models.Model):
    _name = 'lot.number.generator'
    _description = 'Lot Number Generation'
    
    mo_id = fields.Many2one('mrp.production', 'Manufacturing Order', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    lot_number = fields.Char('Lot Number', required=True, index=True)
    box_number = fields.Integer('Box Number')
    catch_weight = fields.Float('Catch Weight')
    label_printed = fields.Boolean('Label Printed', default=False)
    print_job_id = fields.Many2one('label.print.job', 'Print Job')
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)
    
    _sql_constraints = [
        ('lot_number_unique', 'UNIQUE(lot_number)', 
         'Lot number must be unique!')
    ]
    
    @api.model
    def generate_for_mo_split(self, mo, quantity):
        """Generate lot numbers for all units in MO split"""
        lot_records = []
        
        for i in range(quantity):
            lot_number = self._generate_unique_lot_number()
            
            lot_record = self.create({
                'mo_id': mo.id,
                'product_id': mo.product_id.id,
                'lot_number': lot_number,
                'box_number': i + 1,
                'catch_weight': self._get_catch_weight(mo, i),
            })
            lot_records.append(lot_record)
        
        return lot_records
    
    def _generate_unique_lot_number(self):
        """Generate unique lot number with collision prevention"""
        max_attempts = 10
        
        for attempt in range(max_attempts):
            lot_number = self.env['ir.sequence'].next_by_code(
                'lot.number.sequence'
            )
            
            # Check for collision (should be rare with proper sequence config)
            if not self.search([('lot_number', '=', lot_number)]):
                return lot_number
            
            _logger.warning(
                f"Lot number collision detected: {lot_number}. "
                f"Retry attempt {attempt + 1}/{max_attempts}"
            )
        
        raise ValidationError(
            "Unable to generate unique lot number after multiple attempts. "
            "Please contact system administrator."
        )
    
    def _get_catch_weight(self, mo, index):
        """Retrieve catch weight for specific product unit"""
        # Integration with existing catch weight module
        # This is read-only - we don't modify the catch weight module
        catch_weight_data = mo.move_raw_ids[index].catch_weight_info
        return catch_weight_data.weight if catch_weight_data else 0.0
```

### 3. Concurrency Handling

**Database-Level Protection**:
- Use Odoo's `ir.sequence` with `implementation="standard"` (database sequence)
- PostgreSQL sequences are atomic and thread-safe
- No manual locking required

**Application-Level Validation**:
```python
@api.model
def create(self, vals):
    """Ensure lot number uniqueness at creation"""
    if 'lot_number' in vals:
        existing = self.search([('lot_number', '=', vals['lot_number'])])
        if existing:
            raise ValidationError(
                f"Lot number {vals['lot_number']} already exists!"
            )
    return super().create(vals)
```

### 4. Integration with Stock Lot Tracking

```python
def _create_stock_production_lot(self):
    """Create Odoo stock.production.lot records for traceability"""
    StockLot = self.env['stock.production.lot']
    
    for lot_gen in self:
        StockLot.create({
            'name': lot_gen.lot_number,
            'product_id': lot_gen.product_id.id,
            'company_id': lot_gen.mo_id.company_id.id,
            'ref': f"MO: {lot_gen.mo_id.name} - Box {lot_gen.box_number}"
        })
```

## Configuration Options

### System Parameters
Accessible via: `Settings → Technical → Parameters → System Parameters`

| Parameter | Default | Description |
|-----------|---------|-------------|
| `lot.number.prefix` | `LOT` | Lot number prefix |
| `lot.number.include_year` | `True` | Include year in format |
| `lot.number.include_date` | `False` | Include full date (YYYYMMDD) |
| `lot.number.include_product` | `False` | Include product code |
| `lot.number.sequence_padding` | `6` | Number of digits for sequence |

## Validation Rules

### Format Validation
```python
@api.constrains('lot_number')
def _check_lot_number_format(self):
    """Validate lot number matches expected format"""
    pattern = r'^LOT-\d{4}-\d{6}$'
    for record in self:
        if not re.match(pattern, record.lot_number):
            raise ValidationError(
                f"Invalid lot number format: {record.lot_number}. "
                f"Expected format: LOT-YYYY-NNNNNN"
            )
```

### Uniqueness Validation
- Enforced by database constraint: `lot_number_unique`
- Prevents duplicate lot numbers at database level
- Raises clear error message if violation occurs

## Error Handling

### Duplicate Lot Number
**Scenario**: Lot number collision (extremely rare)
**Action**: 
- Log warning with details
- Retry generation with new sequence number
- If max retries exceeded, raise ValidationError

### Sequence Exhaustion
**Scenario**: Sequence reaches maximum value (unlikely with 6 digits)
**Action**:
- Alert administrator
- Provide option to reset sequence (with safeguards)
- Consider increasing sequence padding

## Reporting & Traceability

### Lot Number History Report
Generate report showing:
- All lot numbers generated for date range
- Associated MOs and products
- Catch weights
- Print status
- Current location/status

### Quick Search
```python
def search_by_lot_number(self, lot_number):
    """Quick lookup by lot number for traceability"""
    return self.search([('lot_number', '=', lot_number)])
```

## Performance Considerations
- Lot number generation: O(1) for each number
- Batch generation (200 units): <1 second
- Database index on `lot_number` field for fast lookups
- Minimal database queries (1 per batch generation)

## Related Documents
- [F01: Auto Print on MO Split](F01-auto-print-on-mo-split.md)
- [Database Schema](../reference/database-schema.md)
- [Data Flows](../architecture/data-flows.md)