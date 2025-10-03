"""Safe Print with Automatic Retry

Prints with automatic retry logic and exponential backoff for error recovery.

Source: components/cups-printer.md - Example 75
"""

import cups
import time


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


class CUPSPrinterManager:
    """Placeholder - see cups_printer_manager.py for full implementation"""
    pass