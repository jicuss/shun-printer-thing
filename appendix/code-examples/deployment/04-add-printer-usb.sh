#!/bin/bash
# Add Zebra Printer via USB
#
# Configures Zebra Z230 printer connected via USB to CUPS.
#
# Source: operations/deployment.md - Example 52

# USB connection
sudo lpadmin -p zebra_z230_line1 \
  -E \
  -v usb://Zebra%20Technologies/ZTC%20ZD230-203dpi%20ZPL \
  -m raw

# Set as default
sudo lpadmin -d zebra_z230_line1