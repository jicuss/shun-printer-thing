# Shun Printer - Project Overview

## Project Name
Odoo ERP Label Printing Service for Catch Weight Products

## Executive Summary
Development of a custom Odoo ERP module integrated with an Ubuntu-based Flask print server to enable automated, direct printing of GS1-compliant catch weight product labels to localized Zebra Z230 printers (300 DPI, ZPL) with customizable label templates.

## Business Context
This system serves commissary operations where manufacturing orders (MOs) are split into multiple unique products, each requiring individual lot number tracking and labeling. The solution automates the label printing process that currently requires manual intervention.

## Primary Objective
Implement an automated label printing solution within the Odoo ERP system that prints unique GS1-compliant barcode labels for catch weight products directly to Zebra Z230 (300 DPI) printers when manufacturing orders are split into multiple units.

## Secondary Objectives
- Enable custom label template configuration using Labelary.com ZPL format optimized for 300 DPI
- Automatically trigger batch label printing when MO splits occur (e.g., 200 boxes = 200 labels)
- Ensure each label contains unique lot number and catch weight information
- Provide commissary staff with intuitive interface requiring minimal technical knowledge

## Key Features
1. **Automated Label Generation**: Triggered by MO split events
2. **Unique Lot Numbers**: Sequential generation for each product unit
3. **GS1-128 Barcodes**: Compliant catch weight encoding
4. **Batch Printing**: Handle 200+ labels reliably
5. **Manual Reprints**: Selective or complete reprint capability
6. **Template Management**: CRUD operations for ZPL templates
7. **Job Monitoring**: Real-time status and history tracking

## Success Criteria

### Functional Requirements
- ✓ Labels automatically print when MO is split into multiple units
- ✓ Each label contains unique lot number and accurate catch weight
- ✓ Batch printing works reliably (e.g., 200 labels print successfully)
- ✓ GS1 barcodes are readable and compliant with industry standards
- ✓ Custom templates can be created, saved, and utilized
- ✓ System integrates seamlessly with existing Odoo workflows

### Performance Metrics
- Print job success rate: >95%
- Label generation time: <3 seconds per label
- Batch processing: 200 labels in <10 minutes
- System uptime: 99%+

### User Acceptance
- Intuitive interface requiring minimal training
- Positive user feedback on functionality
- Reduction in labeling errors compared to previous process

## Timeline
- **Accelerated Development**: 2-week development and deployment window
- **Full Project Plan**: 10 weeks (planning through post-launch support)

## Constraints
- Hosted on Odoo SaaS platform (limited server access)
- Must work within Odoo's security and permission framework
- Zebra Z230 printers must be network-accessible or connected via print server
- Labelary.com ZPL format compatibility required (300 DPI)
- Integration with existing catch weight customizations (cannot modify core catch weight logic)

## Assumptions
- Zebra Z230 printers are configured and network-accessible
- Network connectivity between Odoo server and printers is stable
- Commissary staff have appropriate Odoo access rights
- Product master data including catch weights is complete and accurate
- Existing catch weight module properly tracks lot numbers
- MO split functionality is working as expected in current system

## Exclusions
The following items are explicitly excluded from scope:
- Hardware procurement (printers, servers, etc.)
- Network infrastructure setup
- Training on Odoo basics (only module-specific training included)
- Custom Odoo core modifications
- Integration with non-Odoo systems
- Mobile app development

## Related Documents
- [System Architecture](architecture/system-architecture.md)
- [Data Flows](architecture/data-flows.md)
- [Technology Stack](architecture/technology-stack.md)