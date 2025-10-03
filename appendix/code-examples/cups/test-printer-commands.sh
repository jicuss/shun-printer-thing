#!/bin/bash
# CUPS Test Commands
#
# Various commands for testing printer connectivity and status.
#
# Source: components/cups-printer.md - Example 78

# Send test page
lp -d zebra_z230_line1 /usr/share/cups/data/testprint

# Check printer status
lpstat -p zebra_z230_line1 -l

# List all jobs
lpstat -o