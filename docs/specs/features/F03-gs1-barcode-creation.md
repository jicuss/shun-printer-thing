# F03: GS1 Barcode Creation

## Feature Overview
Generate GS1-128 compliant barcodes for catch weight products, encoding all required product information including variable weight in a standardized, scannable format.

## User Story
As a distribution manager, I need GS1-128 barcodes on all product labels so that our products can be scanned and tracked throughout the supply chain, and comply with retail customer requirements.

## Acceptance Criteria
- [ ] Barcodes follow GS1-128 (Code 128) standard
- [ ] All required Application Identifiers (AIs) are included
- [ ] Catch weight is properly encoded with correct decimal precision
- [ ] Barcodes are scannable by standard barcode readers
- [ ] Barcode data strings are validated before label generation
- [ ] System handles variable-length AIs correctly
- [ ] Barcodes include proper FNC1 delimiters

## GS1-128 Format

### Standard Barcode Structure
```
(01)GTIN(10)LOT_NUMBER(3103)WEIGHT(11)PROD_DATE(17)EXP_DATE
```

### Application Identifiers (AIs)

| AI | Description | Format | Example | Required |
|----|-------------|--------|---------|----------|
| 01 | GTIN (Global Trade Item Number) | N14 | 00012345678905 | Yes |
| 10 | Batch/Lot Number | X..20 | LOT-2025-000001 | Yes |
| 310n | Net Weight (kg) | N6 | 001250 (1.250 kg) | Yes |
| 11 | Production Date | N6 (YYMMDD) | 251002 | Optional |
| 17 | Expiration Date | N6 (YYMMDD) | 251102 | Optional |
| 21 | Serial Number | X..20 | SERIAL123 | Optional |

### Weight Encoding (AI 310n)

**Format**: `310n` where `n` indicates decimal places
- `3100`: 0 decimal places (kg)
- `3101`: 1 decimal place (0.1 kg)
- `3102`: 2 decimal places (0.01 kg)  
- `3103`: 3 decimal places (0.001 kg) **[Most Common]**

**Examples**:
- `(3103)001250` = 1.250 kg
- `(3102)12345` = 123.45 kg

## Technical Implementation

### GS1 Data String Generator

> **Code Example**: See [appendix/code-examples/odoo/models/gs1_barcode_generator.py](../../../appendix/code-examples/odoo/models/gs1_barcode_generator.py)

The GS1 barcode generator creates compliant GS1-128 data strings with proper GTIN formatting, weight encoding (AI 3103), and date formatting for production and expiration dates.

## Related Documents
- [F02: Lot Number Generation](F02-lot-number-generation.md)
- [GS1 Standards Reference](../reference/gs1-standards.md)