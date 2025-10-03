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

> **Code Example**: See [appendix/code-examples/odoo/data/lot_number_sequence.xml](../../../appendix/code-examples/odoo/data/lot_number_sequence.xml)

**Odoo Sequence Definition**: Uses year-based prefix with 6-digit padding and date range support for automatic year rollover.

### 2. Generation Logic

> **Code Example**: See [appendix/code-examples/odoo/models/lot_number_generator.py](../../../appendix/code-examples/odoo/models/lot_number_generator.py)

The lot number generator model handles batch generation for MO splits with built-in collision detection, retry logic, and integration with the catch weight module.

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

> **Code Example**: See [appendix/code-examples/odoo/models/stock_lot_integration.py](../../../appendix/code-examples/odoo/models/stock_lot_integration.py)

Creates corresponding stock.production.lot records for full integration with Odoo's inventory tracking system.

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

> **Code Example**: See [appendix/code-examples/odoo/models/lot_number_validation.py](../../../appendix/code-examples/odoo/models/lot_number_validation.py)

Regex-based validation ensures all lot numbers follow the expected format pattern.

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

> **Code Example**: See [appendix/code-examples/odoo/models/lot_number_search.py](../../../appendix/code-examples/odoo/models/lot_number_search.py)

Provides fast lot number lookups for traceability and recall management.

## Performance Considerations
- Lot number generation: O(1) for each number
- Batch generation (200 units): <1 second
- Database index on `lot_number` field for fast lookups
- Minimal database queries (1 per batch generation)

## Related Documents
- [F01: Auto Print on MO Split](F01-auto-print-on-mo-split.md)
- [Database Schema](../reference/database-schema.md)
- [Data Flows](../architecture/data-flows.md)