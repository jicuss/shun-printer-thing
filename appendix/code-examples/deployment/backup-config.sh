#!/bin/bash
# Backup Configuration
#
# Creates backups of Odoo database and Flask server configuration.
#
# Source: operations/deployment.md - Example 61

# Backup Odoo database
# (via Odoo database manager)

# Backup Flask server config
sudo tar -czf label-print-backup.tar.gz /opt/label-print-server