# Database Schema

## Overview
PostgreSQL database schema for Odoo custom module tables.

## Tables

### label_template

Stores ZPL label templates with variable placeholders.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL | Template name |
| code | varchar(100) | UNIQUE, NOT NULL | Template code |
| zpl_code | text | NOT NULL | ZPL template with variables |
| dpi | integer | DEFAULT 300 | Printer DPI |
| width | numeric(5,2) | DEFAULT 4.0 | Label width (inches) |
| height | numeric(5,2) | DEFAULT 6.0 | Label height (inches) |
| active | boolean | DEFAULT true | Active status |
| is_default | boolean | DEFAULT false | Default template flag |
| version | integer | DEFAULT 1 | Template version number |
| previous_version_id | integer | FK label_template | Previous version reference |
| notes | text | | Additional notes |
| create_uid | integer | FK res_users | Created by user |
| create_date | timestamp | DEFAULT now() | Creation timestamp |
| write_uid | integer | FK res_users | Last modified by |
| write_date | timestamp | | Last modification timestamp |

**Indexes**:
- `idx_label_template_code` on `code`
- `idx_label_template_active` on `active`

---

### label_print_job

Tracks all print jobs (automated and manual).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY | Unique identifier |
| mo_id | integer | FK mrp_production | Related MO |
| flask_job_id | varchar(100) | | External Flask job UUID |
| printer_id | integer | FK printer_configuration | Target printer |
| quantity | integer | NOT NULL | Number of labels |
| status | varchar(50) | NOT NULL | Job status |
| job_type | varchar(50) | | Job type (auto/manual/test) |
| labels_data | text | | JSON array of label data |
| current_label | integer | DEFAULT 0 | Current label being printed |
| progress_percent | integer | DEFAULT 0 | Progress percentage |
| error_message | text | | Error details if failed |
| priority | varchar(20) | DEFAULT 'normal' | Job priority |
| submitted_by | integer | FK res_users | User who submitted |
| submitted_date | timestamp | DEFAULT now() | Submission timestamp |
| completed_date | timestamp | | Completion timestamp |
| create_uid | integer | FK res_users | Created by |
| create_date | timestamp | DEFAULT now() | Creation timestamp |

**Indexes**:
- `idx_print_job_status` on `status`
- `idx_print_job_mo` on `mo_id`
- `idx_print_job_date` on `create_date`

**Status Values**:
- `pending`: Job created
- `sent`: Sent to Flask server
- `queued`: In Flask queue
- `printing`: Currently printing
- `completed`: Successfully completed
- `failed`: Failed
- `cancelled`: Cancelled by user

---

### lot_number_generator

Stores generated lot numbers with associated data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY | Unique identifier |
| mo_id | integer | FK mrp_production, NOT NULL | Related MO |
| product_id | integer | FK product_product, NOT NULL | Product |
| lot_number | varchar(100) | UNIQUE, NOT NULL | Generated lot number |
| box_number | integer | NOT NULL | Box sequence number |
| catch_weight | numeric(10,3) | | Variable weight (kg) |
| production_date | date | | Production date |
| expiration_date | date | | Expiration date |
| label_printed | boolean | DEFAULT false | Print status |
| print_job_id | integer | FK label_print_job | Associated print job |
| create_date | timestamp | DEFAULT now() | Creation timestamp |
| create_uid | integer | FK res_users | Created by |

**Indexes**:
- `idx_lot_number` on `lot_number` (UNIQUE)
- `idx_lot_mo` on `mo_id`
- `idx_lot_box_number` on `mo_id, box_number`

---

### printer_configuration

Stores printer configuration details.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL | Printer display name |
| cups_name | varchar(100) | UNIQUE, NOT NULL | CUPS printer name |
| ip_address | varchar(50) | | IP address (network printers) |
| model | varchar(100) | | Printer model |
| dpi | integer | DEFAULT 300 | Printer DPI |
| connection_type | varchar(20) | | USB or Network |
| location | varchar(255) | | Physical location |
| is_default | boolean | DEFAULT false | Default printer flag |
| active | boolean | DEFAULT true | Active status |
| last_status_check | timestamp | | Last status check time |
| status | varchar(50) | | Current status |
| create_date | timestamp | DEFAULT now() | Creation timestamp |
| write_date | timestamp | | Last modification |

**Indexes**:
- `idx_printer_cups_name` on `cups_name` (UNIQUE)
- `idx_printer_active` on `active`

---

### label_template_product_categ_rel

Many-to-many relationship between templates and product categories.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| template_id | integer | FK label_template | Template ID |
| category_id | integer | FK product_category | Category ID |

**Primary Key**: `(template_id, category_id)`

---

### label_template_product_rel

Many-to-many relationship between templates and specific products.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| template_id | integer | FK label_template | Template ID |
| product_id | integer | FK product_product | Product ID |

**Primary Key**: `(template_id, product_id)`

---

## Relationships

```
label_template
  │
  ├── 1:N → label_template (version history)
  └── N:M → product_category (via label_template_product_categ_rel)
  └── N:M → product_product (via label_template_product_rel)

label_print_job
  ├── N:1 → mrp_production
  ├── N:1 → printer_configuration
  ├── N:1 → res_users (submitted_by)
  └── 1:N ← lot_number_generator

lot_number_generator
  ├── N:1 → mrp_production
  ├── N:1 → product_product
  └── N:1 → label_print_job

printer_configuration
  └── 1:N ← label_print_job
```

## SQL Schema

```sql
-- Create sequences
CREATE SEQUENCE lot_number_seq START 1;

-- Constraints and checks
ALTER TABLE label_print_job
  ADD CONSTRAINT chk_progress CHECK (progress_percent BETWEEN 0 AND 100);

ALTER TABLE lot_number_generator
  ADD CONSTRAINT chk_catch_weight CHECK (catch_weight > 0);

ALTER TABLE printer_configuration
  ADD CONSTRAINT chk_dpi CHECK (dpi IN (203, 300, 600));
```

## Related Documents
- [Odoo Module Component](../components/odoo-module.md)
- [System Architecture](../architecture/system-architecture.md)