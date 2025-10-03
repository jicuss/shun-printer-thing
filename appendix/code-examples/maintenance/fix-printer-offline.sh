#!/bin/bash
# Fix Offline Printer
#
# Troubleshooting steps for when printer goes offline.
#
# Source: operations/maintenance.md - Example 63

# Check connection
ping 192.168.1.200

# Resume printer
sudo cupsenable zebra_z230_line1

# Test print
echo "^XA^FO50,50^A0N,50,50^FDTest^FS^XZ" | lp -d zebra_z230_line1 -o raw