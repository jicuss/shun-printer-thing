# GS1 Standards Reference

## GS1-128 Overview

GS1-128 (formerly UCC/EAN-128) is a barcode standard using Code 128 symbology with GS1 Application Identifiers (AIs) to encode product information.

## Application Identifiers (AIs)

### Required for Catch Weight Products

#### (01) GTIN - Global Trade Item Number
**Format**: 14 digits  
**Example**: `00012345678905`

- Must be a valid GTIN-14
- Includes check digit
- Fixed length

#### (10) Batch/Lot Number  
**Format**: Alphanumeric, max 20 characters  
**Example**: `LOT-2025-000001`

- Variable length
- Requires FNC1 separator if followed by another variable-length AI

#### (310n) Net Weight (Variable Measure Trade Item)
**Format**: 6 digits, n indicates decimal places  
**Options**:
- `3100` - 0 decimals (whole kg)
- `3101` - 1 decimal (0.1 kg)
- `3102` - 2 decimals (0.01 kg)  
- `3103` - 3 decimals (0.001 kg) ← **Most common**

**Example**: `(3103)001250` = 1.250 kg

### Optional but Recommended

#### (11) Production Date
**Format**: YYMMDD  
**Example**: `251002` (October 2, 2025)

#### (17) Expiration Date  
**Format**: YYMMDD  
**Example**: `251102` (November 2, 2025)

#### (21) Serial Number
**Format**: Alphanumeric, max 20 characters  
**Example**: `SERIAL123`

### Additional AIs

| AI | Description | Format | Example |
|----|-------------|--------|----------|
| (00) | SSCC | 18 digits | 000123456789012345 |
| (15) | Best Before Date | YYMMDD | 251115 |
| (20) | Product Variant | Numeric, 2 digits | 01 |
| (240) | Additional Product ID | Alphanumeric, max 30 | ADDL123 |
| (400) | Customer PO Number | Alphanumeric, max 30 | PO12345 |
| (3202) | Net Weight (lbs) | 6 digits | 002756 (27.56 lbs) |

## Data String Format

### Human-Readable Format
```
(01)00012345678905(10)LOT-2025-000001(3103)001250(11)251002(17)251102
```

### ZPL/Barcode Format
Remove parentheses, add FNC1 characters:
```
>800012345678905>8LOT2025000001>83103001250110251002170251102
```

**FNC1 character** (`>8` in ZPL):
- Start of barcode
- After variable-length AIs

## Weight Encoding Details

### Decimal Place Selection

Choose based on required precision:

| Precision | AI | Max Weight | Example |
|-----------|-----|------------|----------|
| 1 g | 3103 | 999.999 kg | 1.250 kg = 001250 |
| 10 g | 3102 | 9999.99 kg | 12.50 kg = 001250 |
| 100 g | 3101 | 99999.9 kg | 125.0 kg = 001250 |
| 1 kg | 3100 | 999999 kg | 1250 kg = 001250 |

### Encoding Algorithm

```python
def encode_weight(weight_kg, decimal_places=3):
    """Encode weight for GS1-128"""
    # Convert to integer by shifting decimal
    multiplier = 10 ** decimal_places
    weight_int = int(round(weight_kg * multiplier))
    
    # Format to 6 digits with leading zeros
    return str(weight_int).zfill(6)

# Examples:
encode_weight(1.250, 3)    # "001250"
encode_weight(12.5, 2)      # "001250"  
encode_weight(125.0, 1)     # "001250"
```

## GTIN Structure

### GTIN-14 Format
```
I N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 N12 C
```

- **I**: Indicator digit (packaging level)
- **N1-N12**: Company prefix + item reference
- **C**: Check digit

### Check Digit Calculation

```python
def calculate_gtin_check_digit(gtin_13):
    """Calculate GTIN-14 check digit"""
    digits = [int(d) for d in gtin_13]
    
    # Multiply by 3,1,3,1... pattern
    multipliers = [3,1] * 6 + [3]
    total = sum(d * m for d, m in zip(digits, multipliers))
    
    # Check digit
    check = (10 - (total % 10)) % 10
    return check

# Example:
calculate_gtin_check_digit("0001234567890")  # Returns: 5
# Full GTIN-14: 00012345678905
```

## Compliance Rules

### Fixed vs Variable Length AIs

**Fixed Length** (no FNC1 needed):
- (01) GTIN - 14 digits
- (11) Production Date - 6 digits
- (17) Expiration Date - 6 digits
- (3103) Weight - 6 digits

**Variable Length** (FNC1 required):
- (10) Lot Number - up to 20 chars
- (21) Serial Number - up to 20 chars
- (240) Additional ID - up to 30 chars

### FNC1 Placement

```
Start → (01) → (10) → FNC1 → (3103) → (11) → (17)
  ↑      14     var     ↑       6       6       6
 FNC1          (needs FNC1)
```

## Validation Checklist

- [ ] GTIN has valid check digit
- [ ] Weight is positive and within range
- [ ] Dates are valid (no invalid days/months)
- [ ] Lot number ≤ 20 characters
- [ ] FNC1 after variable-length AIs
- [ ] All required AIs present (01, 10, 310n)
- [ ] Decimal places match AI (e.g., 3103 = 3 decimals)

## Barcode Scanning

### What the Scanner Sees

When scanned, GS1-128 barcodes decode to:
```
]C1 + data string with GS characters
```

**Example**:
```
]C10001234567890510LOT2025000001<GS>3103001250110251002
```

Where `<GS>` (ASCII 29) represents FNC1.

### Parser Example

```python
def parse_gs1_scan(scan_data):
    """Parse scanned GS1-128 data"""
    # Remove ]C1 prefix if present
    if scan_data.startswith(']C1'):
        scan_data = scan_data[3:]
    
    # Replace GS character (ASCII 29) with delimiter
    data = scan_data.replace(chr(29), '|')
    
    # Parse AIs
    result = {}
    pos = 0
    
    while pos < len(data):
        # Read AI (2-4 digits)
        ai = data[pos:pos+2]
        if ai in ['01', '11', '17']:  # Fixed length
            if ai == '01':
                result['gtin'] = data[pos+2:pos+16]
                pos += 16
            elif ai in ['11', '17']:
                result[ai] = data[pos+2:pos+8]
                pos += 8
        # ... handle other AIs
    
    return result
```

## Related Documents
- [F03: GS1 Barcode Creation](../features/F03-gs1-barcode-creation.md)
- [ZPL Templates](zpl-templates.md)