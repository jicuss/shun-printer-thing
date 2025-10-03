#!/bin/bash
# Test Printer Connection
#
# Sends a test ZPL command to verify printer connectivity.
#
# Source: operations/deployment.md - Example 54

echo "^XA^FO50,50^A0N,50,50^FDTest Print^FS^XZ" | lp -d zebra_z230_line1 -o raw