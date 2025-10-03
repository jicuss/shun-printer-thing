#!/bin/bash
# Add Zebra Printer via Network
#
# Configures Zebra Z230 printer connected via network to CUPS.
#
# Source: operations/deployment.md - Example 53

# Network connection
sudo lpadmin -p zebra_z230_line1 \
  -E \
  -v socket://192.168.1.200:9100 \
  -m raw

# Set as default
sudo lpadmin -d zebra_z230_line1