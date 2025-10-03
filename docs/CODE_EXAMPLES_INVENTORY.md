# Code Examples Inventory

This file catalogs all code examples found in the specification documents that should be extracted into the appendix directory structure.

## Status Legend
- ⬜ `TODO` - Not yet processed
- 🔄 `IN_PROGRESS` - Currently being extracted
- ✅ `DONE` - Extracted to appendix
- ⏭️ `SKIP` - Intentionally not extracted (inline example, etc.)

---

## File: features/F01-auto-print-on-mo-split.md

### Example 1: MO Split Detection
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Override
- **Lines**: ~20
- **Suggested Path**: `appendix/code-examples/odoo/models/mrp_production_split.py`
- **Description**: Override of `action_split_production` method to trigger label printing
- **Start Marker**: `class MrpProduction(models.Model):`
- **Key Content**: MO split detection and trigger mechanism

### Example 2: Trigger Label Printing
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/odoo/models/mrp_production_split.py`
- **Description**: `_trigger_label_printing` method
- **Start Marker**: `def _trigger_label_printing(self):`
- **Note**: Can be combined with Example 1

### Example 3: Lot Number Generation
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/odoo/models/lot_number_generation.py`
- **Description**: Sequential lot number generation logic
- **Start Marker**: `def _generate_lot_numbers(self, mo_id, quantity):`

### Example 4: Batch Print Job Creation
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~35
- **Suggested Path**: `appendix/code-examples/odoo/models/print_job_creation.py`
- **Description**: Complete batch print job creation from MO split
- **Start Marker**: `def create_from_mo_split(self, mo):`

### Example 5: API Submission
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~35
- **Suggested Path**: `appendix/code-examples/odoo/models/flask_api_submission.py`
- **Description**: Submit print job to Flask server with error handling
- **Start Marker**: `def _submit_to_print_server(self):`

### Example 6: Status Polling
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/odoo/models/status_polling.py`
- **Description**: Initiate status polling mechanism
- **Start Marker**: `def _start_status_polling(self):`

### Example 7: Label Print Job Data Model
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Definition
- **Lines**: ~20
- **Suggested Path**: `appendix/code-examples/odoo/models/label_print_job.py`
- **Description**: Complete data model for print jobs
- **Start Marker**: `class LabelPrintJob(models.Model):`

---

## File: features/F02-lot-number-generation.md

### Example 8: Sequence Configuration (XML)
- **Status**: ✅ DONE
- **Language**: XML
- **Type**: Odoo Data File
- **Lines**: ~15
- **Suggested Path**: `appendix/code-examples/odoo/data/lot_number_sequence.xml`
- **Description**: Odoo sequence definition for lot numbers
- **Start Marker**: `<odoo>`

### Example 9: Lot Number Generator Model
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Definition
- **Lines**: ~70
- **Suggested Path**: `appendix/code-examples/odoo/models/lot_number_generator.py`
- **Description**: Complete lot number generator model with collision prevention
- **Start Marker**: `class LotNumberGenerator(models.Model):`

### Example 10: Stock Production Lot Integration
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/odoo/models/stock_lot_integration.py`
- **Description**: Create stock.production.lot records for traceability
- **Start Marker**: `def _create_stock_production_lot(self):`

### Example 11: Format Validation
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Constraint Method
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/odoo/models/lot_number_validation.py`
- **Description**: Lot number format validation with regex
- **Start Marker**: `@api.constrains('lot_number')`

### Example 12: Lot Number Search
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~3
- **Suggested Path**: `appendix/code-examples/odoo/models/lot_number_search.py`
- **Description**: Quick lookup by lot number
- **Start Marker**: `def search_by_lot_number(self, lot_number):`

---

## File: features/F03-gs1-barcode-creation.md

### Example 13: GS1 Barcode Generator
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Abstract Model
- **Lines**: ~25
- **Suggested Path**: `appendix/code-examples/odoo/models/gs1_barcode_generator.py`
- **Description**: Complete GS1-128 data string generator
- **Start Marker**: `class GS1BarcodeGenerator(models.AbstractModel):`

---

## File: features/F04-batch-print-queue.md

### Example 14: Flask Queue Manager
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Flask Class
- **Lines**: ~20
- **Suggested Path**: `appendix/code-examples/flask/queue_manager.py`
- **Description**: Print queue management with Redis and RQ
- **Start Marker**: `class PrintQueueManager:`

### Example 15: Print Worker
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Worker Function
- **Lines**: ~25
- **Suggested Path**: `appendix/code-examples/flask/print_worker.py`
- **Description**: Process batch print jobs with retry logic
- **Start Marker**: `def process_batch_print(job_id, job_data):`

### Example 16: Job Resume
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Function
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/flask/job_resume.py`
- **Description**: Resume failed print jobs
- **Start Marker**: `def resume_failed_job(job_id):`

---

## File: features/F05-manual-reprint.md

### Example 17: Reprint Wizard Model
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Wizard (TransientModel)
- **Lines**: ~30
- **Suggested Path**: `appendix/code-examples/odoo/wizards/label_reprint_wizard.py`
- **Description**: Complete reprint wizard with options for all/range/single
- **Start Marker**: `class LabelReprintWizard(models.TransientModel):`

### Example 18: Reprint Job Creation
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~18
- **Suggested Path**: `appendix/code-examples/odoo/models/reprint_job_creation.py`
- **Description**: Create reprint job from lot records
- **Start Marker**: `@api.model`
- **Note**: Part of create_reprint_job method

---

## File: features/F06-template-management.md

### Example 19: ZPL Template Example
- **Status**: ✅ DONE
- **Language**: ZPL
- **Type**: Label Template
- **Lines**: ~15
- **Suggested Path**: `appendix/code-examples/zpl/sample_template.zpl`
- **Description**: Complete ZPL template with variable placeholders
- **Start Marker**: `^XA`

### Example 20: Label Template Model
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Definition
- **Lines**: ~40
- **Suggested Path**: `appendix/code-examples/odoo/models/label_template.py`
- **Description**: Complete template model with versioning
- **Start Marker**: `class LabelTemplate(models.Model):`

### Example 21: Template Engine
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Abstract Model
- **Lines**: ~45
- **Suggested Path**: `appendix/code-examples/odoo/models/template_engine.py`
- **Description**: Template rendering and selection logic
- **Start Marker**: `class LabelTemplateEngine(models.AbstractModel):`

### Example 22: Labelary Preview Integration
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~45
- **Suggested Path**: `appendix/code-examples/odoo/models/labelary_preview.py`
- **Description**: Generate preview using Labelary.com API
- **Start Marker**: `def action_preview_template(self):`

### Example 23: Test Print
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~25
- **Suggested Path**: `appendix/code-examples/odoo/models/test_print.py`
- **Description**: Send test label to printer
- **Start Marker**: `def action_test_print(self):`

### Example 24: Template Versioning
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method Override
- **Lines**: ~18
- **Suggested Path**: `appendix/code-examples/odoo/models/template_versioning.py`
- **Description**: Create new version on ZPL code change
- **Start Marker**: `def write(self, vals):`

### Example 25: Template List View (XML)
- **Status**: ✅ DONE
- **Language**: XML
- **Type**: Odoo View Definition
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/odoo/views/template_list_view.xml`
- **Description**: Tree view for label templates
- **Start Marker**: `<tree string="Label Templates">`

### Example 26: ZPL Syntax Validation
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Constraint Method
- **Lines**: ~15
- **Suggested Path**: `appendix/code-examples/odoo/models/zpl_validation.py`
- **Description**: Basic ZPL syntax validation
- **Start Marker**: `@api.constrains('zpl_code')`

---

## File: features/F07-job-monitoring.md

### Example 27: Status Polling Service
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Abstract Model
- **Lines**: ~65
- **Suggested Path**: `appendix/code-examples/odoo/models/status_poller.py`
- **Description**: Poll Flask server for job status with notifications
- **Start Marker**: `class PrintJobStatusPoller(models.AbstractModel):`

### Example 28: Scheduled Action (Cron XML)
- **Status**: ✅ DONE
- **Language**: XML
- **Type**: Odoo Data File
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/odoo/data/status_polling_cron.xml`
- **Description**: Cron job for polling print job status
- **Start Marker**: `<record id="cron_poll_print_job_status"`

### Example 29: Cron Poll Active Jobs
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/odoo/models/cron_poll_jobs.py`
- **Description**: Poll status for all active jobs
- **Start Marker**: `@api.model`

### Example 30: Progress Display Computed Field
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Field/Method
- **Lines**: ~15
- **Suggested Path**: `appendix/code-examples/odoo/models/progress_display.py`
- **Description**: Computed field for progress display
- **Start Marker**: `class LabelPrintJob(models.Model):`

### Example 31: Dashboard Tree View (XML)
- **Status**: ✅ DONE
- **Language**: XML
- **Type**: Odoo View Definition
- **Lines**: ~20
- **Suggested Path**: `appendix/code-examples/odoo/views/job_dashboard_tree.xml`
- **Description**: Print job dashboard tree view with status decorations
- **Start Marker**: `<tree string="Print Jobs"`

### Example 32: Search/Filter View (XML)
- **Status**: ✅ DONE
- **Language**: XML
- **Type**: Odoo View Definition
- **Lines**: ~20
- **Suggested Path**: `appendix/code-examples/odoo/views/job_search_filters.xml`
- **Description**: Search view with filters and grouping
- **Start Marker**: `<search>`

### Example 33: Error Message Templates
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Python Dictionary + Method
- **Lines**: ~25
- **Suggested Path**: `appendix/code-examples/odoo/models/error_messages.py`
- **Description**: Error message templates and formatting
- **Start Marker**: `ERROR_MESSAGES = {`

### Example 34: Export to CSV
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Odoo Model Method
- **Lines**: ~35
- **Suggested Path**: `appendix/code-examples/odoo/models/export_history_csv.py`
- **Description**: Export print history to CSV
- **Start Marker**: `def action_export_history(self):`

### Example 35: Printer Status Kanban View (XML)
- **Status**: ✅ DONE
- **Language**: XML
- **Type**: Odoo View Definition
- **Lines**: ~25
- **Suggested Path**: `appendix/code-examples/odoo/views/printer_status_kanban.xml`
- **Description**: Kanban view for printer status monitoring
- **Start Marker**: `<record id="view_printer_status_kanban"`

---

## File: operations/testing.md

### Example 36: Test Unique Lot Numbers
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Unit Test (Odoo TransactionCase)
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/tests/test_lot_number_generation.py`
- **Description**: Unit test for lot number uniqueness
- **Start Marker**: `class TestLotNumberGeneration(TransactionCase):`

### Example 37: Test Sequential Numbering
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Unit Test
- **Lines**: ~15
- **Suggested Path**: `appendix/code-examples/tests/test_lot_number_generation.py`
- **Description**: Unit test for sequential lot numbers
- **Start Marker**: `def test_sequential_numbering(self):`
- **Note**: Part of same file as Example 36

### Example 38: Test Weight Encoding
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Unit Test
- **Lines**: ~18
- **Suggested Path**: `appendix/code-examples/tests/test_gs1_barcode.py`
- **Description**: Unit test for GS1 weight encoding
- **Start Marker**: `class TestGS1Barcode(TransactionCase):`

### Example 39: Test GTIN Validation
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Unit Test
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/tests/test_gs1_barcode.py`
- **Description**: Unit test for GTIN check digit validation
- **Start Marker**: `def test_gtin_validation(self):`
- **Note**: Part of same file as Example 38

### Example 40: Flask Test Fixture
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Pytest Fixture
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/tests/test_flask_api.py`
- **Description**: Flask test client fixture
- **Start Marker**: `@pytest.fixture`

### Example 41: Test Print Job Submission
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Flask Test
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/tests/test_flask_api.py`
- **Description**: Test POST /api/print endpoint
- **Start Marker**: `def test_print_job_submission(client):`
- **Note**: Part of same file as Example 40

### Example 42: Test Invalid Printer
- **Status**: ✅ DONE
- **Language**: Python
- **Type**: Flask Test
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/tests/test_flask_api.py`
- **Description**: Test submission to non-existent printer
- **Start Marker**: `def test_invalid_printer(client):`
- **Note**: Part of same file as Example 40

### Example 43: Test MO Split Triggers Print
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Integration Test
- **Lines**: ~22
- **Suggested Path**: `appendix/code-examples/tests/test_integration_mo_split.py`
- **Description**: Test complete MO split to print flow
- **Start Marker**: `def test_mo_split_triggers_print(self):`

### Example 44: Test Odoo-Flask Communication
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Integration Test with Mocks
- **Lines**: ~25
- **Suggested Path**: `appendix/code-examples/tests/test_integration_flask_api.py`
- **Description**: Test Odoo calls Flask API with mocked responses
- **Start Marker**: `@responses.activate`

### Example 45: Test 200 Label Batch Print
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: End-to-End Test
- **Lines**: ~18
- **Suggested Path**: `appendix/code-examples/tests/test_e2e_batch_print.py`
- **Description**: Complete workflow test for 200 label batch
- **Start Marker**: `def test_200_label_batch_print(self):`

### Example 46: Sample Products (Python)
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Test Data
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/tests/test_data.py`
- **Description**: Sample product data for testing
- **Start Marker**: `products = [`

### Example 47: Sample Weights (Python)
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Test Data
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/tests/test_data.py`
- **Description**: Sample catch weight data
- **Start Marker**: `weights = [`
- **Status**: ✅ DONE
- **Note**: Part of same file as Example 46

---

## File: operations/deployment.md

### Example 48: Update System (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/deployment/01-system-update.sh`
- **Description**: Update Ubuntu system packages
- **Start Marker**: `sudo apt update`

### Example 49: Install Dependencies (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/deployment/02-install-dependencies.sh`
- **Description**: Install Docker, CUPS, and Python dependencies
- **Start Marker**: `# Docker`

### Example 50: Configure Firewall (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/deployment/03-configure-firewall.sh`
- **Description**: Configure UFW firewall rules
- **Start Marker**: `# Allow Flask API port`

### Example 51: Netplan Configuration (YAML)
- **Status**: ✅ DONE
- **Language**: YAML
- **Type**: Configuration File
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/deployment/netplan-config.yaml`
- **Description**: Static IP configuration example
- **Start Marker**: `network:`

### Example 52: Add Printer USB (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/deployment/04-add-printer-usb.sh`
- **Description**: Add Zebra printer via USB to CUPS
- **Start Marker**: `# USB connection`

### Example 53: Add Printer Network (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/deployment/05-add-printer-network.sh`
- **Description**: Add Zebra printer via network to CUPS
- **Start Marker**: `# Network connection`

### Example 54: Test Printer (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/deployment/06-test-printer.sh`
- **Description**: Send test print to Zebra printer
- **Start Marker**: `echo "^XA^FO50,50`

### Example 55: requirements.txt
- **Status**: ✅ DONE
- **Language**: Text (pip requirements)
- **Type**: Configuration File
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/deployment/requirements.txt`
- **Description**: Python package requirements for Flask server
- **Start Marker**: `Flask==2.3.3`

### Example 56: .env File
- **Status**: ✅ DONE
- **Language**: Text (env vars)
- **Type**: Configuration File
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/deployment/.env.example`
- **Description**: Environment variables template
- **Start Marker**: `API_KEY=`

### Example 57: Dockerfile
- **Status**: ✅ DONE
- **Language**: Dockerfile
- **Type**: Configuration File
- **Lines**: ~15
- **Suggested Path**: `appendix/code-examples/deployment/Dockerfile`
- **Description**: Docker container definition for Flask app
- **Start Marker**: `FROM python:3.10-slim`

### Example 58: docker-compose.yml
- **Status**: ✅ DONE
- **Language**: YAML
- **Type**: Configuration File
- **Lines**: ~40
- **Suggested Path**: `appendix/code-examples/deployment/docker-compose.yml`
- **Description**: Complete Docker Compose configuration
- **Start Marker**: `version: '3.8'`

### Example 59: Deploy with Docker (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/deployment/07-deploy-docker.sh`
- **Description**: Start Docker Compose services
- **Start Marker**: `sudo docker-compose up -d`

### Example 60: Verify Deployment (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/deployment/08-verify-deployment.sh`
- **Description**: Verify Docker containers and API health
- **Start Marker**: `# Check containers`

### Example 61: Backup Configuration (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/deployment/backup-config.sh`
- **Description**: Backup Odoo DB and Flask server config
- **Start Marker**: `# Backup Odoo database`

---

## File: operations/maintenance.md

### Example 62: Daily Checklist (Bash)
- **Status**: ✅ DONE
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/maintenance/daily-checklist.sh`
- **Description**: Daily system health checks
- **Start Marker**: `# Check services`

### Example 63: Printer Offline Resolution (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/maintenance/fix-printer-offline.sh`
- **Description**: Troubleshoot and fix offline printer
- **Start Marker**: `# Check connection`

### Example 64: Flask Server Restart (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/maintenance/restart-flask.sh`
- **Description**: Restart Flask containers and check health
- **Start Marker**: `# Restart containers`

### Example 65: Daily Backup Script (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/maintenance/daily-backup.sh`
- **Description**: Automated daily backup with cleanup
- **Start Marker**: `#!/bin/bash`

### Example 66: Flask Server Update (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~6
- **Suggested Path**: `appendix/code-examples/maintenance/update-flask.sh`
- **Description**: Update Flask server from git
- **Start Marker**: `cd /opt/label-print-server`

### Example 67: System Updates (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~3
- **Suggested Path**: `appendix/code-examples/maintenance/system-update.sh`
- **Description**: Update system packages and restart Docker
- **Start Marker**: `sudo apt update`

### Example 68: Scale Workers (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/maintenance/scale-workers.sh`
- **Description**: Scale worker containers for performance
- **Start Marker**: `# Increase Flask workers`

### Example 69: CUPS Configuration
- **Status**: ⬜ TODO
- **Language**: Text (Config File)
- **Type**: Configuration File
- **Lines**: ~3
- **Suggested Path**: `appendix/code-examples/maintenance/cups-optimization.conf`
- **Description**: CUPS optimization settings
- **Start Marker**: `MaxJobs 500`

### Example 70: Emergency Recovery (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/maintenance/emergency-recovery.sh`
- **Description**: Complete system recovery from backup
- **Start Marker**: `# Stop services`

---

## File: components/cups-printer.md

### Example 71: Install CUPS (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/cups/install-cups.sh`
- **Description**: Install CUPS and python-cups
- **Start Marker**: `# Install CUPS`

### Example 72: Add Zebra USB (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~6
- **Suggested Path**: `appendix/code-examples/cups/add-zebra-usb.sh`
- **Description**: Add Zebra Z230 via USB
- **Start Marker**: `# USB connection`
- **Note**: Duplicate of Example 52, can reference

### Example 73: Add Zebra Network (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~6
- **Suggested Path**: `appendix/code-examples/cups/add-zebra-network.sh`
- **Description**: Add Zebra Z230 via network
- **Start Marker**: `# Network connection`
- **Note**: Duplicate of Example 53, can reference

### Example 74: CUPS Printer Manager Class
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Python Class
- **Lines**: ~70
- **Suggested Path**: `appendix/code-examples/cups/cups_printer_manager.py`
- **Description**: Complete CUPS printer management class
- **Start Marker**: `class CUPSPrinterManager:`

### Example 75: Safe Print with Retry
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Python Function
- **Lines**: ~20
- **Suggested Path**: `appendix/code-examples/cups/safe_print_retry.py`
- **Description**: Print with automatic retry and exponential backoff
- **Start Marker**: `def safe_print(printer_name, zpl_code, max_retries=3):`

### Example 76: CUPS Status Check (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/cups/check-cups-status.sh`
- **Description**: Check CUPS service status
- **Start Marker**: `systemctl status cups`

### Example 77: View CUPS Logs (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/cups/view-cups-logs.sh`
- **Description**: Tail CUPS error log
- **Start Marker**: `sudo tail -f`

### Example 78: Test Printer Commands (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/cups/test-printer-commands.sh`
- **Description**: Various CUPS test commands
- **Start Marker**: `# Send test page`

### Example 79: Add User to lpadmin (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~3
- **Suggested Path**: `appendix/code-examples/cups/fix-permissions.sh`
- **Description**: Fix CUPS permissions
- **Start Marker**: `sudo usermod`

### Example 80: Clear Print Queue (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~2
- **Suggested Path**: `appendix/code-examples/cups/clear-queue.sh`
- **Description**: Clear stuck print jobs
- **Start Marker**: `cancel -a`

### Example 81: Verify Raw Queue (Python)
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Python Script
- **Lines**: ~6
- **Suggested Path**: `appendix/code-examples/cups/verify_raw_queue.py`
- **Description**: Verify printer is configured as raw queue
- **Start Marker**: `# Verify raw queue`

### Example 82: CUPS Configuration File
- **Status**: ⬜ TODO
- **Language**: Text (Config File)
- **Type**: Configuration File
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/cups/cupsd.conf`
- **Description**: CUPS performance tuning settings
- **Start Marker**: `# Increase max jobs`

### Example 83: Network Printer Optimization (Bash)
- **Status**: ⬜ TODO
- **Language**: Bash
- **Type**: Shell Script
- **Lines**: ~3
- **Suggested Path**: `appendix/code-examples/cups/optimize-network-printer.sh`
- **Description**: Adjust socket timeout for network printer
- **Start Marker**: `# Adjust socket timeout`

---

## File: components/odoo-module.md

### Example 84: __manifest__.py
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Odoo Manifest
- **Lines**: ~35
- **Suggested Path**: `appendix/code-examples/odoo/__manifest__.py`
- **Description**: Complete Odoo module manifest
- **Start Marker**: `# __manifest__.py`

### Example 85: Security Groups (XML)
- **Status**: ⬜ TODO
- **Language**: XML
- **Type**: Odoo Security Definition
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/odoo/security/security.xml`
- **Description**: User groups for label printing
- **Start Marker**: `<!-- security/security.xml -->`

### Example 86: Access Rights (CSV)
- **Status**: ⬜ TODO
- **Language**: CSV
- **Type**: Odoo Access Rights
- **Lines**: ~5
- **Suggested Path**: `appendix/code-examples/odoo/security/ir.model.access.csv`
- **Description**: Model access rights configuration
- **Start Marker**: `id,name,model_id:id`

---

## File: components/flask-api.md

### Example 87: POST /api/print Request (JSON)
- **Status**: ⏭️ SKIP
- **Language**: JSON
- **Type**: API Example
- **Lines**: ~15
- **Reason**: Inline API documentation example

### Example 88: POST /api/print Response (JSON)
- **Status**: ⏭️ SKIP
- **Language**: JSON
- **Type**: API Example
- **Lines**: ~5
- **Reason**: Inline API documentation example

### Example 89: Flask Application (app.py)
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Flask Application
- **Lines**: ~55
- **Suggested Path**: `appendix/code-examples/flask/app.py`
- **Description**: Complete Flask application with all endpoints
- **Start Marker**: `# app.py`

### Example 90: Print Worker (worker.py)
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Worker Script
- **Lines**: ~35
- **Suggested Path**: `appendix/code-examples/flask/worker.py`
- **Description**: RQ worker for processing print jobs
- **Start Marker**: `# worker.py`

### Example 91: API Key Validation
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Python Function
- **Lines**: ~8
- **Suggested Path**: `appendix/code-examples/flask/auth.py`
- **Description**: API key authentication
- **Start Marker**: `API_KEY = os.getenv`

### Example 92: Error Handlers
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Flask Error Handlers
- **Lines**: ~10
- **Suggested Path**: `appendix/code-examples/flask/error_handlers.py`
- **Description**: Flask error handling
- **Start Marker**: `@app.errorhandler(400)`

### Example 93: Logging Configuration
- **Status**: ⬜ TODO
- **Language**: Python
- **Type**: Python Configuration
- **Lines**: ~12
- **Suggested Path**: `appendix/code-examples/flask/logging_config.py`
- **Description**: Rotating file handler for logging
- **Start Marker**: `import logging`

---

## File: architecture/system-architecture.md

### Example 94: Architecture Diagram (ASCII)
- **Status**: ⏭️ SKIP
- **Language**: Text
- **Type**: Diagram
- **Lines**: ~40
- **Reason**: Inline documentation diagram

---

## File: architecture/technology-stack.md

### Example 95: Deployment Architecture Diagram (ASCII)
- **Status**: ⏭️ SKIP
- **Language**: Text
- **Type**: Diagram
- **Lines**: ~20
- **Reason**: Inline documentation diagram

---

## Summary Statistics

- **Total Examples Found**: 95
- **To Extract**: 83
- **To Skip**: 12
- **Files to Create**: ~50-60 (many examples will be combined)

### Breakdown by Type
- Python (Odoo): 42 examples
- Python (Flask): 10 examples
- Python (Tests): 15 examples
- Bash Scripts: 25 examples
- Configuration Files: 10 examples (XML, YAML, CSV, etc.)
- ZPL: 1 example
- JSON (API docs): 2 examples (skipped)
- Diagrams: 2 examples (skipped)

### Breakdown by Category
- Odoo Models/Logic: 30
- Odoo Views/UI: 8
- Odoo Tests: 4
- Flask Server: 10
- CUPS Integration: 10
- Deployment: 15
- Maintenance: 8
- Testing: 10