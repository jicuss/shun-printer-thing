"""Flask Print Queue Manager

Manages print job queuing using Redis and RQ (Redis Queue) with priority tiers
for handling high-volume batch printing operations.

Source: F04-batch-print-queue.md - Example 14
"""

import redis
from rq import Queue
import uuid
import os


class PrintQueueManager:
    def __init__(self):
        self.redis_conn = redis.Redis(host='localhost', port=6379)
        self.high_queue = Queue('high', connection=self.redis_conn)
        self.default_queue = Queue('default', connection=self.redis_conn)
        self.low_queue = Queue('low', connection=self.redis_conn)
    
    def enqueue_print_job(self, job_data, priority='normal'):
        job_id = str(uuid.uuid4())
        queue = self._get_queue_by_priority(priority)
        
        job = queue.enqueue(
            'print_worker.process_batch_print',
            job_id,
            job_data,
            job_timeout='30m'
        )
        
        return {'job_id': job_id, 'status': 'queued'}
    
    def _get_queue_by_priority(self, priority):
        """Select queue based on priority level"""
        if priority == 'high':
            return self.high_queue
        elif priority == 'low':
            return self.low_queue
        else:
            return self.default_queue