# CUPS Printer Component

## Overview
CUPS (Common Unix Printing System) manages the physical connection to Zebra Z230 printers and handles raw ZPL data transmission.

## CUPS Architecture

```
[Flask Worker] → [python-cups] → [CUPS Daemon] → [Printer Driver] → [Zebra Z230]
```

## Installation

### Ubuntu Server

> **Script**: See [appendix/code-examples/cups/install-cups.sh](../../../appendix/code-examples/cups/install-cups.sh)

## Printer Configuration

### Add Zebra Z230 to CUPS

**Via Command Line**:

> **Scripts**:
> - USB: [appendix/code-examples/cups/add-zebra-usb.sh](../../../appendix/code-examples/cups/add-zebra-usb.sh)
> - Network: [appendix/code-examples/cups/add-zebra-network.sh](../../../appendix/code-examples/cups/add-zebra-network.sh)

**Via Web Interface**:
1. Navigate to `http://localhost:631`
2. Administration → Add Printer
3. Select Zebra Z230 from discovered printers
4. Choose "Raw Queue" as driver
5. Set printer name: `zebra_z230_line1`

### Printer Settings
- **Driver**: Raw/passthrough (no processing)
- **Resolution**: 300 DPI
- **Paper Size**: Continuous (label roll)
- **Duplex**: Off

## Python Integration

### Basic CUPS Operations

> **Code Example**: See [appendix/code-examples/cups/cups_printer_manager.py](../../../appendix/code-examples/cups/cups_printer_manager.py)

Complete Python class for managing CUPS printers including listing, status checks, and raw ZPL printing.

### Error Handling

> **Code Example**: See [appendix/code-examples/cups/safe_print_retry.py](../../../appendix/code-examples/cups/safe_print_retry.py)

Prints with automatic retry logic and exponential backoff for error recovery.

## Troubleshooting

### Check CUPS Service Status

> **Script**: See [appendix/code-examples/cups/check-cups-status.sh](../../../appendix/code-examples/cups/check-cups-status.sh)

### View CUPS Logs

> **Script**: See [appendix/code-examples/cups/view-cups-logs.sh](../../../appendix/code-examples/cups/view-cups-logs.sh)

### Test Printer Connection

> **Script**: See [appendix/code-examples/cups/test-printer-commands.sh](../../../appendix/code-examples/cups/test-printer-commands.sh)

### Common Issues

**Printer Not Found**:
- Check USB connection or network connectivity
- Run `lpinfo -v` to list available devices

**Permission Denied**:

> **Script**: See [appendix/code-examples/cups/fix-permissions.sh](../../../appendix/code-examples/cups/fix-permissions.sh)

**Jobs Stuck in Queue**:

> **Script**: See [appendix/code-examples/cups/clear-queue.sh](../../../appendix/code-examples/cups/clear-queue.sh)

## Raw ZPL Printing

### Why Raw Mode?
- CUPS should not process or interpret ZPL
- Zebra printers expect raw ZPL commands
- Prevents corruption of barcode data

### Verification

> **Code Example**: See [appendix/code-examples/cups/verify_raw_queue.py](../../../appendix/code-examples/cups/verify_raw_queue.py)

## Performance Tuning

### CUPS Configuration

> **Config File**: See [appendix/code-examples/cups/cupsd.conf](../../../appendix/code-examples/cups/cupsd.conf)

Edit `/etc/cups/cupsd.conf` and add these performance tuning settings.

### Network Printer Optimization

> **Script**: See [appendix/code-examples/cups/optimize-network-printer.sh](../../../appendix/code-examples/cups/optimize-network-printer.sh)

## Related Documents
- [System Architecture](../architecture/system-architecture.md)
- [Flask API Component](flask-api.md)
- [Deployment Guide](../operations/deployment.md)