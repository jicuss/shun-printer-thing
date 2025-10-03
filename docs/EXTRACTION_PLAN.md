# Code Examples Extraction Plan

This file organizes the 83 code examples into logical groups for systematic extraction.

## Group 1: Core Odoo Models (F01-F03) - 13 examples
**Priority**: High - Foundation models
**Estimated time**: 15-20 minutes

- Example 1: MO Split Detection (F01)
- Example 2: Trigger Label Printing (F01) - combine with Ex1
- Example 3: Lot Number Generation (F01)
- Example 4: Batch Print Job Creation (F01)
- Example 5: API Submission (F01)
- Example 6: Status Polling (F01)
- Example 7: Label Print Job Data Model (F01)
- Example 8: Sequence Configuration XML (F02)
- Example 9: Lot Number Generator Model (F02)
- Example 10: Stock Production Lot Integration (F02)
- Example 11: Format Validation (F02)
- Example 12: Lot Number Search (F02)
- Example 13: GS1 Barcode Generator (F03)

## Group 2: Print Queue & Reprint (F04-F05) - 5 examples
**Priority**: High - Core functionality
**Estimated time**: 10 minutes

- Example 14: Flask Queue Manager (F04)
- Example 15: Print Worker (F04)
- Example 16: Job Resume (F04)
- Example 17: Reprint Wizard Model (F05)
- Example 18: Reprint Job Creation (F05)

## Group 3: Template Management (F06) - 8 examples
**Priority**: Medium - Configuration layer
**Estimated time**: 15 minutes

- Example 19: ZPL Template Example (F06)
- Example 20: Label Template Model (F06)
- Example 21: Template Engine (F06)
- Example 22: Labelary Preview Integration (F06)
- Example 23: Test Print (F06)
- Example 24: Template Versioning (F06)
- Example 25: Template List View XML (F06)
- Example 26: ZPL Syntax Validation (F06)

## Group 4: Job Monitoring (F07) - 9 examples
**Priority**: Medium - Operational visibility
**Estimated time**: 15 minutes

- Example 27: Status Polling Service (F07)
- Example 28: Scheduled Action Cron XML (F07)
- Example 29: Cron Poll Active Jobs (F07)
- Example 30: Progress Display Computed Field (F07)
- Example 31: Dashboard Tree View XML (F07)
- Example 32: Search/Filter View XML (F07)
- Example 33: Error Message Templates (F07)
- Example 34: Export to CSV (F07)
- Example 35: Printer Status Kanban View XML (F07)

## Group 5: Testing Suite - 12 examples
**Priority**: Medium - Quality assurance
**Estimated time**: 15 minutes

- Example 36: Test Unique Lot Numbers
- Example 37: Test Sequential Numbering (combine with Ex36)
- Example 38: Test Weight Encoding
- Example 39: Test GTIN Validation (combine with Ex38)
- Example 40: Flask Test Fixture
- Example 41: Test Print Job Submission (combine with Ex40)
- Example 42: Test Invalid Printer (combine with Ex40)
- Example 43: Test MO Split Triggers Print
- Example 44: Test Odoo-Flask Communication
- Example 45: Test 200 Label Batch Print
- Example 46: Sample Products
- Example 47: Sample Weights (combine with Ex46)

## Group 6: Deployment Scripts - 14 examples
**Priority**: High - Getting system running
**Estimated time**: 15 minutes

- Example 48: Update System
- Example 49: Install Dependencies
- Example 50: Configure Firewall
- Example 51: Netplan Configuration
- Example 52: Add Printer USB
- Example 53: Add Printer Network
- Example 54: Test Printer
- Example 55: requirements.txt
- Example 56: .env File
- Example 57: Dockerfile
- Example 58: docker-compose.yml
- Example 59: Deploy with Docker
- Example 60: Verify Deployment
- Example 61: Backup Configuration

## Group 7: Maintenance Scripts - 9 examples
**Priority**: Medium - Operations
**Estimated time**: 10 minutes

- Example 62: Daily Checklist
- Example 63: Printer Offline Resolution
- Example 64: Flask Server Restart
- Example 65: Daily Backup Script
- Example 66: Flask Server Update
- Example 67: System Updates
- Example 68: Scale Workers
- Example 69: CUPS Configuration
- Example 70: Emergency Recovery

## Group 8: CUPS Integration - 13 examples
**Priority**: High - Printer communication
**Estimated time**: 15 minutes

- Example 71: Install CUPS
- Example 72: Add Zebra USB (reference to Ex52)
- Example 73: Add Zebra Network (reference to Ex53)
- Example 74: CUPS Printer Manager Class
- Example 75: Safe Print with Retry
- Example 76: CUPS Status Check
- Example 77: View CUPS Logs
- Example 78: Test Printer Commands
- Example 79: Add User to lpadmin
- Example 80: Clear Print Queue
- Example 81: Verify Raw Queue
- Example 82: CUPS Configuration File
- Example 83: Network Printer Optimization

## Group 9: Flask API & Odoo Module Config - 7 examples
**Priority**: High - Core integration
**Estimated time**: 10 minutes

- Example 84: __manifest__.py
- Example 85: Security Groups XML
- Example 86: Access Rights CSV
- Example 89: Flask Application (app.py)
- Example 90: Print Worker (worker.py)
- Example 91: API Key Validation
- Example 92: Error Handlers
- Example 93: Logging Configuration

---

## Total: 9 Groups, 83 Examples

**Recommended order of execution**:
1. Group 1 (Core models - foundation)
2. Group 6 (Deployment - can test immediately)
3. Group 9 (Flask API - complete the integration)
4. Group 8 (CUPS - printer layer)
5. Group 2 (Queue & reprint)
6. Group 3 (Templates)
7. Group 4 (Monitoring)
8. Group 5 (Testing)
9. Group 7 (Maintenance)