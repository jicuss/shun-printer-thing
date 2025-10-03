#!/bin/bash
# Configure UFW Firewall
#
# Opens necessary ports for Flask API and optionally CUPS web interface.
#
# Source: operations/deployment.md - Example 50

# Allow Flask API port
sudo ufw allow 5000/tcp

# Allow CUPS web interface (optional)
sudo ufw allow 631/tcp

# Enable firewall
sudo ufw enable