# CUPS Printer Component

## Overview
CUPS (Common Unix Printing System) manages the physical connection to Zebra Z230 printers and handles raw ZPL data transmission.

## CUPS Architecture

```
[Flask Worker] → [python-cups] → [CUPS Daemon] → [Printer Driver] → [Zebra Z230]
```

## Installation

### Ubuntu Server
```bash
# Install CUPS
sudo apt update
sudo apt install cups cups-client

# Install python-cups
pip install pycups

# Start CUPS service
sudo systemctl start cups
sudo systemctl enable cups
```

## Printer Configuration

### Add Zebra Z230 to CUPS

**Via Command Line**:
```bash
# USB connection
lpadmin -p zebra_z230_line1 \
  -E \
  -v usb://Zebra%20Technologies/ZTC%20ZD230-203dpi%20ZPL \
  -m raw

# Network connection  
lpadmin -p zebra_z230_line1 \
  -E \
  -v socket://192.168.1.100:9100 \
  -m raw

# Set as default (optional)
lpadmin -d zebra_z230_line1
```

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

```python
import cups

class CUPSPrinterManager:
    def __init__(self):
        self.conn = cups.Connection()
    
    def list_printers(self):
        """Get all configured printers"""
        printers = self.conn.getPrinters()
        return [
            {
                'name': name,
                'state': info.get('printer-state-message', 'Unknown'),
                'accepting': info.get('printer-is-accepting-jobs', False)
            }
            for name, info in printers.items()
        ]
    
    def get_printer_status(self, printer_name):
        """Check if printer is online and accepting jobs"""
        try:
            attrs = self.conn.getPrinterAttributes(printer_name)
            state = attrs.get('printer-state', 0)
            
            # State codes: 3=idle, 4=processing, 5=stopped
            if state == 3:
                return 'idle'
            elif state == 4:
                return 'printing'
            elif state == 5:
                return 'stopped'
            else:
                return 'unknown'
                
        except cups.IPPError as e:
            return f'error: {e}'
    
    def print_raw_zpl(self, printer_name, zpl_code, job_title="Label"):
        """Send raw ZPL to printer"""
        import tempfile
        import os
        
        # Create temporary file with ZPL
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.zpl',
            delete=False
        ) as f:
            f.write(zpl_code)
            temp_path = f.name
        
        try:
            # Submit print job
            job_id = self.conn.printFile(
                printer_name,
                temp_path,
                job_title,
                {'raw': 'true'}  # Important: disable all processing
            )
            return job_id
            
        except cups.IPPError as e:
            raise Exception(f"Print failed: {e}")
            
        finally:
            # Clean up temp file
            os.unlink(temp_path)
    
    def cancel_job(self, printer_name, job_id):
        """Cancel a print job"""
        try:
            self.conn.cancelJob(job_id)
            return True
        except cups.IPPError:
            return False
    
    def get_jobs(self, printer_name):
        """Get current jobs in printer queue"""
        try:
            jobs = self.conn.getJobs(
                which_jobs='not-completed',
                my_jobs=False,
                requested_attributes=['job-id', 'job-name', 'job-state']
            )
            return jobs
        except cups.IPPError:
            return {}
```

### Error Handling

```python
def safe_print(printer_name, zpl_code, max_retries=3):
    """Print with automatic retry on failure"""
    manager = CUPSPrinterManager()
    
    for attempt in range(max_retries):
        try:
            # Check printer status first
            status = manager.get_printer_status(printer_name)
            if status == 'stopped':
                raise Exception("Printer is stopped/offline")
            
            # Attempt to print
            job_id = manager.print_raw_zpl(printer_name, zpl_code)
            return job_id
            
        except cups.IPPError as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                raise Exception(f"Failed after {max_retries} attempts: {e}")
```

## Troubleshooting

### Check CUPS Service Status
```bash
systemctl status cups
```

### View CUPS Logs
```bash
sudo tail -f /var/log/cups/error_log
```

### Test Printer Connection
```bash
# Send test page
lp -d zebra_z230_line1 /usr/share/cups/data/testprint

# Check printer status
lpstat -p zebra_z230_line1 -l

# List all jobs
lpstat -o
```

### Common Issues

**Printer Not Found**:
- Check USB connection or network connectivity
- Run `lpinfo -v` to list available devices

**Permission Denied**:
- Add user to `lpadmin` group:
  ```bash
  sudo usermod -a -G lpadmin $USER
  ```

**Jobs Stuck in Queue**:
- Clear queue: `cancel -a zebra_z230_line1`
- Restart CUPS: `sudo systemctl restart cups`

## Raw ZPL Printing

### Why Raw Mode?
- CUPS should not process or interpret ZPL
- Zebra printers expect raw ZPL commands
- Prevents corruption of barcode data

### Verification
```python
# Verify raw queue is configured
import cups
conn = cups.Connection()
attrs = conn.getPrinterAttributes('zebra_z230_line1')
print(attrs.get('printer-make-and-model'))  # Should show "Raw Queue"
```

## Performance Tuning

### CUPS Configuration
Edit `/etc/cups/cupsd.conf`:
```
# Increase max jobs
MaxJobs 500

# Job retention
MaxJobTime 3600
JobRetryLimit 5
JobRetryInterval 30
```

### Network Printer Optimization
```bash
# Adjust socket timeout
lpadmin -p zebra_z230_line1 -o printer-op-policy=default \
  -o socket-timeout=60
```

## Related Documents
- [System Architecture](../architecture/system-architecture.md)
- [Flask API Component](flask-api.md)
- [Deployment Guide](../operations/deployment.md)