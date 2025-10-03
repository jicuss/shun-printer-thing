#!/bin/bash
# Scale Worker Containers
#
# Increases the number of worker containers for better performance.
#
# Source: operations/maintenance.md - Example 68

# Increase Flask workers
sudo docker-compose up -d --scale worker=6