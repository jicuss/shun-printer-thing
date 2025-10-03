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

```python
class GS1BarcodeGenerator(models.AbstractModel):
    _name = 'gs1.barcode.generator'
    
    @api.model
    def generate_gs1_data_string(self, product, lot_number, catch_weight, 
                                  production_date=None, expiration_date=None):
        """Generate complete GS1-128 data string"""
        
        gtin = self._format_gtin(product.barcode)
        lot = lot_number
        weight = self._encode_weight(catch_weight, decimal_places=3)
        prod_date = self._format_date(production_date or fields.Date.today())
        
        data_string = f"(01){gtin}(10){lot}(3103){weight}(11){prod_date}"
        
        if expiration_date:
            exp_date = self._format_date(expiration_date)
            data_string += f"(17){exp_date}"
        
        self._validate_gs1_data_string(data_string)
        return data_string
    
    def _format_gtin(self, barcode):
        if not barcode:
            raise ValidationError("Product must have a barcode/GTIN")
        gtin = ''.join(filter(str.isdigit, barcode))
        return gtin.zfill(14)
    
    def _encode_weight(self, weight, decimal_places=3):
        multiplier = 10 ** decimal_places
        weight_int = int(round(weight * multiplier))
        return str(weight_int).zfill(6)
    
    def _format_date(self, date):
        if isinstance(date, str):
            date = fields.Date.from_string(date)
        return date.strftime('%y%m%d')
```

## Related Documents
- [F02: Lot Number Generation](F02-lot-number-generation.md)
- [GS1 Standards Reference](../reference/gs1-standards.md)