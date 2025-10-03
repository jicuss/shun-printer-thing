"""Job Resume Functionality

Resumes failed print jobs by retrieving failed label indices and creating
a new high-priority job for only the failed labels.

Source: F04-batch-print-queue.md - Example 16
"""

from redis import Redis

redis_conn = Redis(host='localhost', port=6379)


def resume_failed_job(job_id, original_labels, enqueue_func):
    """Resume a failed job by reprinting only failed labels"""
    failed_indices = redis_conn.lrange(f"job:{job_id}:failed", 0, -1)
    failed_labels = [original_labels[int(i)-1] for i in failed_indices]
    
    # Create new high-priority job for failed labels
    return enqueue_func(
        {'labels': failed_labels, 'printer': job_data['printer']}, 
        priority='high'
    )