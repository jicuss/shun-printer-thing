#!/bin/bash
# Add Zebra Z230 via USB to CUPS
#
# Note: This is a reference to the deployment script.
# See: appendix/code-examples/deployment/04-add-printer-usb.sh
#
# Source: components/cups-printer.md - Example 72 (reference to Example 52)

# USB connection
sudo lpadmin -p zebra_z230_line1 \
  -E \
  -v usb://Zebra%20Technologies/ZTC%20ZD230-203dpi%20ZPL \
  -m raw

# Set as default
sudo lpadmin -d zebra_z230_line1