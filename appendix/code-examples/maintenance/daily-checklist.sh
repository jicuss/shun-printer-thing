#!/bin/bash
# Daily System Health Checklist
#
# Runs daily checks on services, logs, and disk space.
#
# Source: operations/maintenance.md - Example 62

# Check services
sudo docker-compose ps
systemctl status cups
lpstat -p zebra_z230_line1

# Check logs
sudo tail -50 /opt/label-print-server/logs/flask.log | grep -i error

# Check disk space
df -h