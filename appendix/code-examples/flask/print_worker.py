"""Print Worker for Batch Processing

RQ worker that processes print jobs from the queue, handles label printing
via CUPS, tracks progress, and manages retries for failed labels.

Source: F04-batch-print-queue.md - Example 15
"""

import cups
import time
from redis import Redis
import logging

redis_conn = Redis(host='localhost', port=6379)
_logger = logging.getLogger(__name__)


def process_batch_print(job_id, job_data):
    """Process a batch print job with progress tracking"""
    printer_name = job_data['printer']
    labels = job_data['labels']
    
    # Update status
    redis_conn.hset(f"job:{job_id}", 'status', 'printing')
    
    # Initialize CUPS
    conn = cups.Connection()
    
    try:
        for idx, label in enumerate(labels, 1):
            # Update progress
            redis_conn.hset(f"job:{job_id}", 'current_label', idx)
            
            # Print with retry
            success = print_single_label(conn, printer_name, label['zpl_code'])
            
            if not success:
                redis_conn.rpush(f"job:{job_id}:failed", idx)
                _logger.error(f"Failed to print label {idx} for job {job_id}")
            
            time.sleep(0.1)  # Prevent printer overload
        
        # Mark complete
        redis_conn.hset(f"job:{job_id}", 'status', 'completed')
        
    except Exception as e:
        redis_conn.hset(f"job:{job_id}", 'status', 'failed')
        redis_conn.hset(f"job:{job_id}", 'error', str(e))
        raise


def print_single_label(conn, printer, zpl_code, max_retries=3):
    """Print single label with retry logic"""
    import tempfile
    import os
    
    for attempt in range(max_retries):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.zpl', delete=False) as f:
                f.write(zpl_code)
                temp_path = f.name
            
            try:
                conn.printFile(printer, temp_path, "Label", {'raw': 'true'})
                return True
            finally:
                os.unlink(temp_path)
                
        except cups.IPPError as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                _logger.error(f"Failed after {max_retries} attempts: {e}")
                return False
    
    return False