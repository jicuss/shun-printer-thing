#!/bin/bash
# Restart Flask Server
#
# Restarts Flask containers and verifies health.
#
# Source: operations/maintenance.md - Example 64

# Restart containers
sudo docker-compose restart

# Check health
curl http://localhost:5000/api/health

# Check logs
sudo docker-compose logs --tail=100