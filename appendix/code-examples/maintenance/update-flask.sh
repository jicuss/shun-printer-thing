#!/bin/bash
# Update Flask Server
#
# Pulls latest code and rebuilds containers.
#
# Source: operations/maintenance.md - Example 66

cd /opt/label-print-server
sudo git pull
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d