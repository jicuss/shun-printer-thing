#!/bin/bash
# Emergency Recovery
#
# Complete system recovery from backup.
#
# Source: operations/maintenance.md - Example 70

# Stop services
sudo docker-compose down

# Restore from backup
sudo tar -xzf /backup/config-latest.tar.gz -C /

# Restart
sudo docker-compose up -d

# Verify
curl http://localhost:5000/api/health