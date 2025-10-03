
Shun Takeda
4:58 PM (19 minutes ago)
to me

Functional Success
✓ Labels automatically print when MO is split into multiple units
✓ Each label contains unique lot number and accurate catch weight
✓ Batch printing works reliably (e.g., 200 labels print successfully)
✓ GS1 barcodes are readable and compliant with industry standards
✓ Custom# Scope of Work: Odoo ERP Label Printing Service
Project Overview
Development of a custom Odoo ERP module integrated with an Ubuntu-based Flask print server to enable automated, direct printing of GS1-compliant catch weight product labels to localized Zebra Z230 printers (300 DPI, ZPL) with customizable label templates. This system will serve commissary operations where manufacturing orders are split into multiple unique products, each requiring individual lot number tracking and labeling.
System Architecture
Odoo Cloud (Custom Module)
    ↓ HTTPS POST Request (JSON with label data)
Ubuntu Print Server (Flask + CUPS + Docker)
    ↓ CUPS Print Job (Raw ZPL)
Zebra Z230 Printer (300 DPI, USB or Network)
1. Project Objectives
Primary Objective
Implement an automated label printing solution within the Odoo ERP system that prints unique GS1-compliant barcode labels for catch weight products directly to Zebra Z230 (300 DPI) printers when manufacturing orders are split into multiple units.
Secondary Objectives
Enable custom label template configuration using Labelary.com ZPL format optimized for 300 DPI
Automatically trigger batch label printing when MO splits occur (e.g., 200 boxes = 200 labels)
Ensure each label contains unique lot number and catch weight information
Provide commissary staff with intuitive interface requiring minimal technical knowledge
2. Technical Specifications
Technology Stack
Platform: Odoo ERP (hosted via Odoo SaaS platform) with custom catch weight module
Programming Language: Python (Odoo module + Flask server)
Database: PostgreSQL (Odoo), SQLite or Redis (Print server job queue)
Print Server OS: Ubuntu Server 20.04 LTS or newer
Print Server Framework: Flask or FastAPI (Python web framework)
Print Management: CUPS (Common Unix Printing System)
Containerization: Docker + Docker Compose
Label Design: Labelary.com ZPL (Zebra Programming Language)
Printer Model: Zebra Z230 (300 DPI, ZPL compatible)
Barcode Standard: GS1-128 compliant barcodes
System Architecture Components
Component 1: Odoo Custom Module (Cloud-Hosted)
Detects Manufacturing Order (MO) split events
Generates unique lot numbers for each split unit
Retrieves catch weight data from product records
Generates GS1 barcode data strings
Populates ZPL templates with product data
Makes HTTPS POST requests to Flask print server
Logs print job status and history
Provides UI for manual reprints
Component 2: Ubuntu Print Server (Local Network)
Flask/FastAPI web service running in Docker container
Receives print requests via REST API (HTTPS)
Manages print job queue
Interfaces with CUPS for printer communication
Sends raw ZPL code to Zebra Z230 printer
Returns print job status to Odoo
Monitors printer health and availability
Provides API for printer status checks
Component 3: CUPS (Print Management)
Installed on Ubuntu server (can be containerized or native)
Manages Zebra Z230 printer connection (USB or network)
Handles raw ZPL data transmission
Provides printer status monitoring
Manages print queue and error handling
3. Key Features & Deliverables
3.1 Odoo Custom Module Development
3.1.1 Manufacturing Order Integration
Event listener/hook for MO split operations
Automatic detection when MO is divided into multiple units (e.g., 200 boxes)
Trigger print job creation upon MO split completion
Integration with existing catch weight module (read-only, no modifications)
3.1.2 Lot Number Management
Automatic generation of unique lot numbers for each split unit
Sequential numbering system (e.g., LOT-2024-001, LOT-2024-002...)
Lot number validation and duplicate prevention
Storage of lot number associations with products and MO
3.1.3 GS1 Barcode Data Generation
Support for GS1-128 barcode format
Configurable Application Identifiers (AIs) specific to catch weight:
GTIN (01) - Global Trade Item Number
Batch/Lot Number (10) - Required for each unique product
Net Weight (310n) - Catch weight variable measure
Production Date (11)
Expiration Date (17)
Serial Number (21) - If required for traceability
Additional AIs as required
Barcode validation and GS1 compliance checking
Automatic barcode data string generation from product data
Variable weight encoding in GS1 format (proper decimal handling)
3.1.4 ZPL Template Management
Database storage for ZPL templates (PostgreSQL)
Template CRUD interface (Create, Read, Update, Delete)
Template assignment rules (by product category, catch weight range, production line)
Variable/placeholder system for dynamic data insertion:
{PRODUCT_NAME} - Product name
{SKU} - Product SKU/code
{LOT_NUMBER} - Unique lot number (auto-generated)
{WEIGHT} - Catch weight/variable weight
{GS1_BARCODE} - GS1-128 barcode data string
{PRODUCTION_DATE} - Production date (formatted)
{EXPIRATION_DATE} - Expiration date (formatted)
{MO_REFERENCE} - Manufacturing Order reference number
{BOX_NUMBER} - Box number in sequence (e.g., "Box 1 of 200")
Custom fields specific to commissary operations
Template preview functionality using Labelary.com API (300 DPI)
Default template assignment for product types
Template versioning and history
3.1.5 Print Server Communication
HTTPS client for secure communication with Flask print server
REST API calls to print server endpoints:
POST /api/print - Submit print job
GET /api/status/{job_id} - Check job status
GET /api/printers - List available printers
JSON payload structure for print requests
Error handling and retry logic (3 attempts with exponential backoff)
Timeout handling (30 seconds per request)
API authentication (API key or token-based)
3.1.6 Print Job Management
Print job queue/history table in PostgreSQL
Job status tracking: Pending, Sent, Printing, Completed, Failed
Batch print job creation (e.g., 200 labels = 1 batch job)
Progress tracking for large batch prints
Failed job retry mechanism
Print job logging with timestamps
3.1.7 User Interface Components
Automatic Print Trigger: No user interaction needed when MO splits
Manual Reprint Interface:
Reprint button in Manufacturing Order view
Select specific box numbers to reprint (e.g., boxes 45-50)
Reprint all labels for entire MO
Print Job Dashboard:
View recent print jobs and status
Filter by date, MO, status
Export print history to CSV
Template Management UI:
For administrators/supervisors only
Create/edit/delete templates
Test print functionality
Template assignment configuration
Printer Status Widget:
Real-time printer status display
Online/offline indicator
Recent error messages
Simplified Touch-Friendly Interface for commissary floor use
Visual Confirmation: Toast notifications for successful prints
Error Notifications: Clear error messages with troubleshooting hints
3.2 Flask Print Server Development (Ubuntu Server)
3.2.1 REST API Endpoints
POST /api/print
- Accepts: JSON with ZPL code, printer name, quantity, job metadata
- Returns: Job ID, status, estimated completion time
- Validates: ZPL syntax, printer availability, queue capacity

GET /api/status/{job_id}
- Returns: Job status, progress, error messages
- Includes: Timestamp, printer used, labels printed

GET /api/printers
- Returns: List of available printers with status
- Includes: Name, model, connection type, current status

POST /api/test
- Accepts: Printer name
- Sends test label to verify connectivity
- Returns: Success/failure status

GET /api/health
- Health check endpoint
- Returns: Server status, CUPS status, printer statuses

POST /api/reprint/{job_id}
- Resubmits a previous print job
- Returns: New job ID
3.2.2 Print Queue Management
Queue system for handling multiple concurrent print jobs
Priority handling (urgent vs standard jobs)
Rate limiting to prevent printer overload
Automatic retry for failed jobs (3 attempts)
Job cancellation capability
Queue persistence (survives server restarts)
3.2.3 CUPS Integration
Python CUPS library integration (python-cups)
Raw ZPL data transmission to printer
Printer discovery and configuration
Printer status monitoring (online/offline, paper out, ribbon low)
Error detection and reporting
Support for both USB and network-connected printers
3.2.4 Error Handling & Logging
Comprehensive error logging (to file and console)
Categorized error messages:
Network errors (Odoo communication issues)
Printer errors (offline, paper jam, ribbon out)
ZPL syntax errors
CUPS errors
Automatic error notification to Odoo
Log rotation and retention (30 days)
Debug mode for troubleshooting
3.2.5 Security
HTTPS only (SSL/TLS certificate required)
API key authentication for all endpoints
IP whitelist for Odoo server
Rate limiting to prevent abuse
Input validation and sanitization
Secure logging (no sensitive data in logs)
3.2.6 Docker Containerization
Docker container for Flask application
Docker Compose for multi-container setup (Flask + Redis/database if needed)
Volume mounts for persistent data (logs, queue state)
Auto-restart policy
Health checks in Docker configuration
Easy deployment and updates
3.3 Ubuntu Server Setup & Configuration
3.3.1 Server Requirements
Ubuntu Server 20.04 LTS or newer
Minimum 2GB RAM
20GB disk space
Static IP address on commissary network
Network connectivity to Zebra Z230 printer
Reliable power supply (UPS recommended)
3.3.2 Software Installation
Docker and Docker Compose
CUPS (Common Unix Printing System)
Zebra printer drivers (if needed)
SSL/TLS certificates (Let's Encrypt or self-signed)
Python 3.8+ (for Flask server)
System monitoring tools (optional: htop, netdata)
3.3.3 Printer Configuration
Add Zebra Z230 to CUPS
Configure printer as "raw" device (no processing)
Set default printer settings (300 DPI, continuous feed)
Test print functionality
Configure printer sharing if multiple production lines
3.3.4 Network Configuration
Configure static IP address
Open firewall port for Flask API (e.g., 5000 or 443)
Configure DNS (if using domain name)
Set up port forwarding if Odoo is external
VPN configuration (if required for security)
3.4 Integration & Testing Components
3.4.1 End-to-End Testing
Test MO split with various quantities (1, 10, 50, 200 labels)
Verify unique lot number generation
Validate GS1 barcode compliance (use barcode scanner)
Test catch weight data accuracy
Verify all 200 labels print correctly in batch
Test reprint functionality
Simulate printer offline scenarios
Test error handling and recovery
3.4.2 Performance Testing
Measure label generation time (target: <500ms per label)
Measure print queue throughput (target: 200 labels in <10 minutes)
Test concurrent print jobs (multiple MOs splitting simultaneously)
Monitor server resource usage under load
Test network latency between Odoo and print server
3.4.3 User Acceptance Testing
Commissary staff test in real production environment
Verify labels are readable and accurate
Test reprint workflow
Validate error message clarity
Gather feedback on UI/UX
4. Functional Requirements
4.1 Automated Label Generation Process (MO Split)
Manufacturing Order is processed and split into multiple units (e.g., 200 boxes)
System detects MO split event via Odoo workflow hook/trigger
Odoo custom module generates unique lot numbers for each of the 200 products
For each product unit, the module:
Retrieves catch weight data from Odoo product record
Generates unique lot number (sequential or based on defined pattern)
Retrieves product master data (name, SKU, GTIN, dates, etc.)
Generates GS1-128 barcode data string with all required AIs
Populates ZPL template with all variable data
Creates complete ZPL label code
Module creates batch print job containing all 200 labels
Module makes HTTPS POST request to Flask print server with:
JSON payload containing all label ZPL codes
Printer name/identifier
Job metadata (MO reference, quantity, priority)
Authentication credentials
Flask print server receives request and:
Validates request and authentication
Adds job to print queue
Returns job ID and estimated completion time to Odoo
Print server sends ZPL codes to CUPS
CUPS transmits raw ZPL to Zebra Z230 printer
Labels print sequentially
Print server updates job status (in progress, completed)
Odoo module polls print server for job status updates
Odoo displays confirmation message to commissary staff upon completion
Job is logged in print history with timestamp and status
4.2 Manual Label Reprinting
Commissary staff opens Manufacturing Order in Odoo
Clicks "Reprint Labels" button
Interface displays options:
Reprint all labels for this MO
Reprint specific range (e.g., boxes 45-50)
Reprint single label by box number
Staff selects option and confirms
System follows same process as automated printing (steps 4-14 above)
Confirmation displayed when complete
4.3 Template Configuration (Admin Only)
Administrator logs into Odoo with appropriate permissions
Navigates to "Label Templates" menu
CRUD operations available:
Create: Upload ZPL code, define variables, set 300 DPI, assign to product categories
Read: View existing templates and their assignments
Update: Modify ZPL code or template settings
Delete: Remove unused templates (with confirmation)
Test print functionality:
Select template
Provide sample data for variables
Preview using Labelary.com API (300 DPI rendering)
Send test label to printer
Template assignment rules:
Assign template to product category
Assign template to specific SKUs
Set default template for production line
Priority order if multiple templates match
4.4 Data Integration Points
Odoo Product Master: Pull product name, SKU, GTIN, category
Catch Weight Module: Read catch weight/variable weight data (read-only, no modifications to existing module)
Manufacturing (MRP) Module: Detect MO split events, read MO reference number
Lot Number Tracking: Generate and store lot numbers, link to products and MO
Inventory Module: Update inventory with new lot numbers (if required)
User Management: Check permissions for reprint and template management functions
4.5 Print Server Data Management
Job Queue: Store pending print jobs in memory or database
Job History: Log all print jobs with metadata for audit trail (30-day retention)
Printer Configuration: Store printer names, IP addresses, connection details
Status Cache: Cache printer status to reduce CUPS polling
5. Technical Deliverables
5.1 Odoo Custom Module Package
Deliverable: Complete Odoo module ready for installation
Components:
Module structure following Odoo development guidelines (version-specific)
__manifest__.py with proper dependencies and metadata
Models:
label.template - Store ZPL templates
print.job - Track print jobs and status
lot.number.sequence - Manage lot number generation
Views:
Manufacturing Order form view with print/reprint buttons
Label template management interface (list, form, kanban)
Print job dashboard (list view with filters)
Printer status widget
Controllers:
HTTP endpoints for Labelary preview integration
Print server communication handler
Business logic:
MO split event detection (automated trigger)
Lot number generation algorithm
GS1 barcode data string generator
ZPL template engine (variable replacement)
Print server API client
Job status polling mechanism
Security:
Access rights configuration (ir.model.access.csv)
Record rules for data isolation
User group definitions (admin, supervisor, operator)
Static assets:
JavaScript for UI interactions
CSS for custom styling
Icons and images
Tests (optional but recommended):
Unit tests for barcode generation
Integration tests for MO split detection
API client tests
Installation package: .zip file containing all module files
5.2 Flask Print Server Application
Deliverable: Dockerized Flask application ready for deployment
Components:
app.py - Main Flask application with all API endpoints
requirements.txt - Python dependencies
Dockerfile - Container definition
docker-compose.yml - Multi-container orchestration
Configuration files:
config.py - Environment-specific settings
.env.example - Template for environment variables
Modules:
printer_manager.py - CUPS integration logic
queue_manager.py - Print queue handling
auth.py - API authentication
logger.py - Logging configuration
Utils:
zpl_validator.py - ZPL syntax checking (optional)
error_handler.py - Centralized error handling
Health check script for Docker
Startup/shutdown scripts
5.3 Ubuntu Server Setup Scripts
Deliverable: Automated setup and configuration scripts
Components:
setup_server.sh - Initial server setup (install Docker, CUPS, etc.)
configure_cups.sh - CUPS configuration and printer setup
deploy_print_server.sh - Deploy Flask container
ssl_setup.sh - SSL certificate configuration
backup_script.sh - Backup configuration and data
update_script.sh - Update print server to new version
System service files (systemd) for auto-start
Firewall configuration script (ufw)
5.4 Database Schema Documentation
Deliverable: Complete database schema for Odoo module
Tables:
label.template
id (integer, primary key)
name (varchar, required) - Template name
zpl_code (text, required) - ZPL template with variables
dpi (integer, default 300) - Printer DPI
active (boolean, default true) - Active status
product_categ_ids (many2many) - Assigned product categories
default_template (boolean) - Is this the default template
created_date, modified_date (datetime)
created_by, modified_by (many2one res.users)
print.job
id (integer, primary key)
job_id (varchar, unique) - External job ID from print server
mo_id (many2one mrp.production) - Related Manufacturing Order
printer_name (varchar) - Target printer
quantity (integer) - Number of labels
status (selection) - pending, sent, printing, completed, failed
priority (selection) - normal, high, urgent
zpl_data (text) - Complete ZPL code (for reprints)
error_message (text) - Error details if failed
submitted_date, completed_date (datetime)
submitted_by (many2one res.users)
lot.number.generation
id (integer, primary key)
mo_id (many2one mrp.production)
product_id (many2one product.product)
lot_number (varchar, unique, indexed)
box_number (integer) - Sequential box number
catch_weight (float) - Variable weight
label_printed (boolean) - Print status
print_job_id (many2one print.job)
created_date (datetime)
printer.configuration (optional - for multi-printer setups)
id (integer, primary key)
name (varchar, required)
ip_address (varchar)
model (varchar) - Printer model
production_line (varchar) - Associated line
is_default (boolean)
active (boolean)
5.5 API Documentation
Deliverable: Complete API specification
Odoo → Flask Print Server API:
POST /api/print
Request Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json

Request Body:
{
  "printer": "zebra_z230_line1",
  "quantity": 200,
  "labels": [
    {
      "zpl_code": "^XA^FO50,50^A0N,50,50^FDLabel 1^FS^XZ",
      "box_number": 1,
      "lot_number": "LOT-2024-001",
      "metadata": {...}
    },
    ...
  ],
  "job_metadata": {
    "mo_reference": "MO/2024/001",
    "priority": "normal"
  }
}

Response:
{
  "job_id": "uuid-string",
  "status": "pending",
  "estimated_completion": "2024-10-15T14:30:00Z",
  "message": "Print job queued successfully"
}
GET /api/status/{job_id}
Response:
{
  "job_id": "uuid-string",
  "status": "printing",
  "progress": {
    "total": 200,
    "completed": 150,
    "failed": 0
  },
  "started_at": "2024-10-15T14:25:00Z",
  "estimated_completion": "2024-10-15T14:30:00Z"
}
GET /api/printers
Response:
{
  "printers": [
    {
      "name": "zebra_z230_line1",
      "model": "Zebra Z230",
      "status": "online",
      "connection": "USB",
      "jobs_in_queue": 2
    }
  ]
}
5.6 Documentation Package
Deliverable: Complete documentation suite
Technical Documentation:
System architecture diagram
Data flow diagrams
API specifications
Database schema documentation
Deployment guide for Ubuntu server
Docker deployment guide
Odoo module installation guide
Security configuration guide
Backup and recovery procedures
User Documentation:
Commissary Staff Quick Start Guide (PDF with screenshots)
How to reprint labels
What to do if labels don't print
Understanding error messages
Administrator Guide (PDF)
Template creation and management
Printer configuration
User access management
Troubleshooting common issues
ZPL Template Creation Guide
ZPL basics for 300 DPI Zebra printers
Variable syntax and usage
Example templates for common products
Labelary.com integration guide
GS1 barcode positioning best practices
Training Materials:
PowerPoint presentation for commissary staff training
Video walkthrough of key workflows (optional)
Hands-on exercises for testing
Maintenance Documentation:
Server maintenance checklist
Update procedures
Log file locations and analysis
Performance monitoring guide
Common error codes and solutions
5.7 Testing & Quality Assurance
Deliverable: Test results and QA reports
Test Deliverables:
Unit test results for Odoo module
Integration test results (Odoo ↔ Print Server)
End-to-end test results (full workflow)
Performance test results (batch printing benchmarks)
Load test results (concurrent job handling)
User acceptance test (UAT) report with commissary staff feedback
Barcode scan test results (GS1 compliance verification)
Edge case test results (printer offline, network issues, etc.), ip_address, model, workstation_id, production_line, etc.)
Print job history/logging table (job_id, mo_id, timestamp, quantity, status, printer_id, etc.)
Lot number tracking table (lot_id, mo_id, product_id, catch_weight, box_number, label_printed, etc.)
5.3 Integration Components
Zebra Z230 printer communication service (ZPL over network socket or USB)
Labelary API integration for ZPL preview/validation (300 DPI)
GS1 barcode library/generator implementation with catch weight support
MO split event listener/webhook
Batch print job queue manager
Lot number generation service
5.4 Documentation
Technical documentation for module installation and configuration
User manual for commissary staff (simplified, visual)
Administrator guide for template creation and printer setup
ZPL template examples for common catch weight products
API documentation for any custom endpoints
Troubleshooting guide for common printing issues
Training materials with screenshots and workflows
6. Constraints & Assumptions
Constraints
Hosted on Odoo SaaS platform (limited server access)
Must work within Odoo's security and permission framework
Zebra Z230 printers must be network-accessible or connected via print server
Labelary.com ZPL format compatibility required (300 DPI)
Accelerated timeline: 2-week development and deployment window
Integration with existing catch weight customizations (cannot modify core catch weight logic)
Assumptions
Zebra Z230 printers are configured and network-accessible
Network connectivity between Odoo server and printers is stable
Commissary staff have appropriate Odoo access rights
Product master data including catch weights is complete and accurate
Existing catch weight module properly tracks lot numbers
MO split functionality is working as expected in current system
Commissary workstations have reliable network/power
Label stock (appropriate size for Zebra Z230) is available
7. Success Criteria
Functional Success
✓ Labels print successfully to designated local printers
✓ GS1 barcodes are readable and compliant with industry standards
✓ Custom templates can be created, saved, and utilized
✓ System integrates seamlessly with existing Odoo workflows
Performance Metrics
Print job success rate: >95%
Label generation time: <3 seconds
Template loading time: <2 seconds
System uptime: 99%+
User Acceptance
Intuitive interface requiring minimal training
Positive user feedback on functionality
Reduction in labeling errors compared to previous process
8. Project Phases
Phase 1: Planning & Design (Week 1-2)
Finalize technical requirements
Design database schema
Create wireframes for UI components
Select GS1 barcode library
Phase 2: Core Development (Week 3-6)
Develop custom Odoo module structure
Implement GS1 barcode generation
Create template management interface
Build printer integration layer
Phase 3: Testing & Refinement (Week 7-8)
Unit testing of all components
Integration testing with Odoo workflows
User acceptance testing
Bug fixes and performance optimization
Phase 4: Deployment & Training (Week 9-10)
Deploy to production environment
User training sessions
Documentation delivery
Post-launch support
9. Risks & Mitigation
Risk
Impact
Mitigation Strategy
Printer connectivity issues
High
Implement robust error handling and fallback to PDF generation
Odoo hosting limitations
Medium
Design solution compatible with SaaS constraints; evaluate client-side printing if needed
GS1 compliance complexity
Medium
Use established GS1 libraries and conduct thorough testing
Template compatibility issues
Low
Provide template validation and comprehensive examples
10. Support & Maintenance
Post-Launch Support
30-day warranty period for bug fixes
Technical support for configuration issues
Template creation assistance
Ongoing Maintenance (Optional)
Regular updates for Odoo version compatibility
New feature additions as requested
Performance monitoring and optimization
11. Exclusions
The following items are explicitly excluded from this scope:
Hardware procurement (printers, servers, etc.)
Network infrastructure setup
Training on Odoo basics (only module-specific training included)
Custom Odoo core modifications
Integration with non-Odoo systems
Mobile app development
Document Version: 1.0
Last Updated: October 2, 2025
Status: Draft
