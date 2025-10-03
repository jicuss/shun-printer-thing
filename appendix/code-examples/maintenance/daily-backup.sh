#!/bin/bash
# Daily Backup Script
#
# Automated daily backup with cleanup of old backups.
#
# Source: operations/maintenance.md - Example 65

BACKUP_DIR="/backup/label-print"
DATE=$(date +%Y%m%d)

# Backup config
sudo tar -czf "$BACKUP_DIR/config-$DATE.tar.gz" /opt/label-print-server

# Backup Redis
sudo docker-compose exec redis redis-cli SAVE

# Clean old backups (30 days)
find "$BACKUP_DIR" -mtime +30 -delete