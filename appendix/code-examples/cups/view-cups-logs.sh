#!/bin/bash
# View CUPS Error Logs
#
# Tails the CUPS error log for troubleshooting.
#
# Source: components/cups-printer.md - Example 77

sudo tail -f /var/log/cups/error_log