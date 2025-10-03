#!/bin/bash
# Add Zebra Z230 via Network to CUPS
#
# Note: This is a reference to the deployment script.
# See: appendix/code-examples/deployment/05-add-printer-network.sh
#
# Source: components/cups-printer.md - Example 73 (reference to Example 53)

# Network connection
sudo lpadmin -p zebra_z230_line1 \
  -E \
  -v socket://192.168.1.200:9100 \
  -m raw

# Set as default
sudo lpadmin -d zebra_z230_line1