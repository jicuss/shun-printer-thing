# ZPL Templates

## ZPL Overview

ZPL (Zebra Programming Language) is a page description language for Zebra thermal printers. ZPL II is the current version.

## Basic ZPL Structure

```zpl
^XA           // Start of label
^FO50,50      // Field Origin (x,y coordinates)
^A0N,30,30    // Font (0=default, N=normal, height, width)
^FDHello      // Field Data
^FS           // Field Separator
^XZ           // End of label
```

## Common ZPL Commands

### Label Control
- `^XA` - Start of label format
- `^XZ` - End of label format
- `^LH` - Label Home (set origin)
- `^PW` - Print Width
- `^LL` - Label Length

### Field Positioning
- `^FO` - Field Origin (x, y in dots)
- `^FS` - Field Separator (end field)

### Text
- `^A` - Font selection
  - `^A0N,h,w` - Default font, Normal, height, width
- `^FD` - Field Data (actual text content)
- `^FN` - Field Number (for variable data)

### Barcodes
- `^BC` - Code 128 barcode
  - `^BC,h,Y,N,N` - height, print interpretation line, above/below, check digit
- `^BY` - Bar code field default
  - `^BY,w,r,h` - module width, ratio, height

### Graphics
- `^GB` - Graphic Box (rectangle)
- `^GF` - Graphic Field (image data)

## 300 DPI Considerations

**Resolution**: 300 DPI = 300 dots per inch

**Conversion**:
- 1 inch = 300 dots
- 1 cm = 118 dots
- 1 mm = 11.8 dots

**Example**: 4" x 6" label
- Width: 4 × 300 = 1200 dots
- Height: 6 × 300 = 1800 dots

## Variable Placeholder System

### Syntax
Variables use curly brace notation: `{VARIABLE_NAME}`

### Standard Variables

| Variable | Description | Example |
|----------|-------------|----------|
| `{PRODUCT_NAME}` | Product name | "Wild Caught Salmon" |
| `{SKU}` | Product SKU | "SALM-001" |
| `{LOT_NUMBER}` | Lot number | "LOT-2025-000001" |
| `{WEIGHT}` | Catch weight | "1.250" |
| `{WEIGHT_UNIT}` | Weight unit | "kg" |
| `{GS1_BARCODE}` | GS1 barcode data | (ZPL format) |
| `{GS1_HUMAN_READABLE}` | Human-readable GS1 | "(01)00012..." |
| `{PRODUCTION_DATE}` | Production date | "2025-10-02" |
| `{EXPIRATION_DATE}` | Expiration date | "2025-11-02" |
| `{BOX_NUMBER}` | Box number | "Box 1 of 200" |
| `{MO_REFERENCE}` | MO reference | "MO/2025/001" |
| `{COMPANY_NAME}` | Company name | "ABC Commissary" |

## Example Templates

### Basic Catch Weight Label (4" x 6")

```zpl
^XA
^PW1200
^LL1800

// Company Header
^FO50,50^A0N,40,40^FD{COMPANY_NAME}^FS
^FO50,100^GB1100,3,3^FS

// Product Information
^FO50,150^A0N,50,50^FD{PRODUCT_NAME}^FS
^FO50,220^A0N,35,35^FDSKU: {SKU}^FS

// Lot and Weight
^FO50,290^A0N,40,40^FDLot: {LOT_NUMBER}^FS
^FO50,350^A0N,50,50^FDWeight: {WEIGHT} {WEIGHT_UNIT}^FS

// GS1-128 Barcode
^FO50,450^BY3,3,150
^BCN,150,Y,N,N
^FD{GS1_BARCODE}^FS

// Human-Readable Barcode Data
^FO50,630^A0N,25,25^FD{GS1_HUMAN_READABLE}^FS

// Production Info
^FO50,700^A0N,30,30^FDProduced: {PRODUCTION_DATE}^FS
^FO50,750^A0N,30,30^FDExpires: {EXPIRATION_DATE}^FS

// Box Number
^FO50,820^A0N,30,30^FD{BOX_NUMBER}^FS
^FO50,870^A0N,25,25^FDMO: {MO_REFERENCE}^FS

^XZ
```

### Compact Label (3" x 2")

```zpl
^XA
^PW900
^LL600

^FO30,30^A0N,30,30^FD{PRODUCT_NAME}^FS
^FO30,70^A0N,25,25^FD{LOT_NUMBER}^FS
^FO30,110^A0N,30,30^FD{WEIGHT} {WEIGHT_UNIT}^FS

^FO30,170^BY2,2,80
^BCN,80,Y,N,N
^FD{GS1_BARCODE}^FS

^FO30,280^A0N,20,20^FD{PRODUCTION_DATE}^FS

^XZ
```

### Label with Border and Logo Area

```zpl
^XA
^PW1200
^LL1800

// Border
^FO20,20^GB1160,1760,5^FS

// Logo placeholder (150x150)
^FO50,50^GB150,150,3^FS
^FO75,100^A0N,25,25^FDLOGO^FS

// Product name (large)
^FO230,70^A0N,60,60^FD{PRODUCT_NAME}^FS

// Data section with box
^FO50,250^GB1100,400,3^FS
^FO70,280^A0N,35,35^FDLot: {LOT_NUMBER}^FS
^FO70,340^A0N,45,45^FDWeight: {WEIGHT} kg^FS
^FO70,410^A0N,30,30^FDProduced: {PRODUCTION_DATE}^FS
^FO70,460^A0N,30,30^FDExpires: {EXPIRATION_DATE}^FS
^FO70,530^A0N,30,30^FD{BOX_NUMBER}^FS

// Barcode
^FO100,700^BY4,3,180
^BCN,180,Y,N,N
^FD{GS1_BARCODE}^FS

// Footer
^FO50,1700^A0N,25,25^FD{COMPANY_NAME} | {MO_REFERENCE}^FS

^XZ
```

## Testing Templates

### Labelary.com API

Preview ZPL without printing:

```bash
curl -X POST \
  'http://api.labelary.com/v1/printers/12dpmm/labels/4x6/0/' \
  --data-binary @label.zpl \
  -H 'Accept: image/png' \
  -o label.png
```

**DPI to dpmm conversion**:
- 203 DPI = 8 dpmm
- 300 DPI = 12 dpmm
- 600 DPI = 24 dpmm

### Test Print Command

```bash
# Send ZPL directly to printer
echo "^XA^FO50,50^A0N,50,50^FDTest^FS^XZ" | lp -d zebra_z230_line1 -o raw
```

## Best Practices

1. **Use ^FO for all positioning** - Don't rely on default positions
2. **Test at actual DPI** - Preview at 300 DPI, not 203 DPI
3. **Leave margins** - Minimum 20 dots from edge
4. **Barcode sizing** - Ensure minimum quiet zones (10 dots)
5. **Font readability** - Minimum 20pt for body text
6. **Variable length** - Account for long product names
7. **Consistent spacing** - Use grid system (e.g., 50-dot increments)

## Troubleshooting

**Barcode won't scan**:
- Check quiet zones (white space before/after)
- Verify FNC1 characters in GS1 barcodes
- Increase barcode height

**Text cut off**:
- Check label dimensions (^PW, ^LL)
- Verify field positions don't exceed label size

**Inconsistent printing**:
- Clean printer head
- Calibrate media sensors
- Check darkness setting

## Related Documents
- [F06: Template Management](../features/F06-template-management.md)
- [GS1 Standards](gs1-standards.md)