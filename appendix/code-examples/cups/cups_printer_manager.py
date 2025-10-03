"""CUPS Printer Manager Class

Complete Python class for managing CUPS printers including listing, status checks,
and raw ZPL printing.

Source: components/cups-printer.md - Example 74
"""

import cups
import tempfile
import os


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