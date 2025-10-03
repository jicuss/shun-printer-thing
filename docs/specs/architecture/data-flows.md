# Data Flows

## Flow 1: Automated Print on MO Split

### Trigger
User splits Manufacturing Order into multiple product units in Odoo

### Sequence

```
[User] → [Odoo MRP] → [Custom Module] → [Flask API] → [CUPS] → [Printer]
```

**Step-by-Step**:

1. **MO Split Event**
   - User: Splits MO into 200 boxes
   - Odoo: Fires split completion event
   - Data: MO ID, product ID, quantity (200)

2. **Event Detection**
   - Module: Listens for MO split webhook/signal
   - Action: Triggers label generation workflow

3. **Lot Number Generation**
   - Module: Creates 200 unique lot numbers
   - Pattern: `LOT-{YEAR}-{SEQUENCE}` (e.g., LOT-2025-001)
   - Storage: Saved to `lot.number.generation` table
   - Links: Associated with MO ID and product IDs

4. **Product Data Retrieval**
   - For each of 200 units:
     - Product name, SKU, GTIN
     - Catch weight (from catch weight module)
     - Production date, expiration date
     - Box number (1 of 200, 2 of 200, etc.)

5. **GS1 Barcode Generation**
   - For each unit:
     - Construct GS1-128 data string
     - Include AIs: GTIN (01), Lot (10), Weight (310n), Dates (11/17)
     - Validate compliance
     - Format: `(01)00012345678905(10)LOT-2025-001(3103)001250(11)251002`

6. **ZPL Template Population**
   - Retrieve appropriate template for product category
   - For each label:
     - Replace `{PRODUCT_NAME}` with actual product name
     - Replace `{LOT_NUMBER}` with generated lot number
     - Replace `{WEIGHT}` with catch weight
     - Replace `{GS1_BARCODE}` with barcode data string
     - Replace `{BOX_NUMBER}` with "Box 1 of 200", etc.
   - Result: 200 complete ZPL code strings

7. **Print Job Creation**
   - Create `print.job` record in Odoo database
   - Status: "pending"
   - Store: MO ID, quantity (200), ZPL data

8. **API Request to Flask**
   - Endpoint: `POST /api/print`
   - Headers: `Authorization: Bearer {API_KEY}`
   - Payload:
     ```json
     {
       "printer": "zebra_z230_line1",
       "quantity": 200,
       "labels": [
         {"zpl_code": "^XA...", "box_number": 1, "lot_number": "LOT-2025-001"},
         {"zpl_code": "^XA...", "box_number": 2, "lot_number": "LOT-2025-002"},
         ...
       ],
       "job_metadata": {
         "mo_reference": "MO/2025/001",
         "priority": "normal"
       }
     }
     ```

9. **Flask Processing**
   - Validate API key and request structure
   - Generate unique job ID (UUID)
   - Add to print queue
   - Return response:
     ```json
     {
       "job_id": "550e8400-e29b-41d4-a716-446655440000",
       "status": "queued",
       "estimated_completion": "2025-10-02T15:30:00Z"
     }
     ```

10. **Odoo Job Tracking**
    - Update `print.job` record with Flask job ID
    - Status: "sent"
    - Begin polling Flask for status updates

11. **Flask → CUPS → Printer**
    - Flask: Dequeues job, sends ZPL to CUPS
    - CUPS: Transmits raw ZPL to Zebra Z230
    - Printer: Prints labels sequentially
    - Flask: Updates job status every 10 labels

12. **Completion**
    - Flask: Marks job as "completed"
    - Odoo: Polls and receives completion status
    - Odoo: Updates job record, displays success notification
    - Module: Marks all 200 `lot.number.generation` records as printed

### Data Entities Involved
- `mrp.production` (Manufacturing Order)
- `product.product` (Product master data)
- `stock.production.lot` (Lot/serial numbers)
- `label.template` (ZPL templates)
- `print.job` (Print job tracking)
- `lot.number.generation` (Lot number details)

## Flow 2: Manual Reprint

### Trigger
Commissary staff clicks "Reprint Labels" button on MO

### Sequence

1. **UI Interaction**
   - Staff: Opens MO in Odoo
   - Staff: Clicks "Reprint Labels"
   - UI: Displays reprint options dialog

2. **Reprint Selection**
   - Options:
     - Reprint all (200 labels)
     - Reprint range (boxes 45-50)
     - Reprint single (box 47)
   - Staff: Selects option and confirms

3. **Data Retrieval**
   - Module: Queries `lot.number.generation` table
   - Filter: By MO ID and selected box numbers
   - Retrieves: Lot numbers, catch weights, product data

4. **ZPL Regeneration**
   - Module: Uses same template as original print
   - Populates with retrieved data
   - Creates ZPL code(s) for selected labels

5. **Print Job Submission**
   - Follows same process as automated print (steps 7-12 above)
   - New `print.job` record created
   - Sent to Flask API

### Data Entities Involved
- Same as Flow 1, plus user action audit trail

## Flow 3: Template Management

### Trigger
Administrator creates or updates ZPL template

### Sequence

1. **Template CRUD**
   - Admin: Navigates to Label Templates menu
   - Admin: Creates new or edits existing template
   - UI: ZPL code editor with syntax highlighting

2. **Template Data**
   - Name: "Catch Weight Seafood 4x6"
   - ZPL Code: Raw ZPL with variables `{PRODUCT_NAME}`, `{LOT_NUMBER}`, etc.
   - DPI: 300
   - Product Categories: Assigned categories

3. **Validation**
   - Module: Checks for required variables
   - Module: Validates ZPL syntax (optional)

4. **Preview** (Optional)
   - Admin: Clicks "Preview"
   - Module: Provides sample data for variables
   - Module: Calls Labelary.com API with sample ZPL
   - UI: Displays rendered label preview (300 DPI PNG)

5. **Test Print** (Optional)
   - Admin: Clicks "Test Print"
   - Module: Generates single test label
   - Sends to Flask API → printer

6. **Save**
   - Record saved to `label.template` table
   - Assignment rules updated

### Data Entities Involved
- `label.template`
- `product.category` (for template assignment)

## Related Documents
- [System Architecture](system-architecture.md)
- [F01: Auto Print on MO Split](../features/F01-auto-print-on-mo-split.md)
- [F05: Manual Reprint](../features/F05-manual-reprint.md)