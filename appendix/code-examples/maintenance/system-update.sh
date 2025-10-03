#!/bin/bash
# System Updates
#
# Updates system packages and restarts Docker.
#
# Source: operations/maintenance.md - Example 67

sudo apt update && sudo apt upgrade -y
sudo systemctl restart docker