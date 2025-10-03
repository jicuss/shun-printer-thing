"""Verify Raw Queue Configuration

Checks that printer is configured as a raw queue without processing.

Source: components/cups-printer.md - Example 81
"""

import cups

# Verify raw queue is configured
conn = cups.Connection()
attrs = conn.getPrinterAttributes('zebra_z230_line1')
print(attrs.get('printer-make-and-model'))  # Should show "Raw Queue"