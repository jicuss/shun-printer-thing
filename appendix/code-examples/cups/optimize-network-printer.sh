#!/bin/bash
# Network Printer Optimization
#
# Adjusts socket timeout for network printers.
#
# Source: components/cups-printer.md - Example 83

# Adjust socket timeout
lpadmin -p zebra_z230_line1 -o printer-op-policy=default \
  -o socket-timeout=60