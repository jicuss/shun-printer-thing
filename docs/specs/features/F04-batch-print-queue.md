# F04: Batch Print Queue Management

## Feature Overview
Manage high-volume batch printing jobs (e.g., 200 labels) through a queuing system that ensures reliable, sequential printing with progress tracking and error recovery.

## User Story
As a commissary operator, when I split an MO into 200 units, I want all labels to print reliably in order so that I can match labels to physical boxes without confusion or delays.

## Acceptance Criteria
- [ ] System queues batch jobs for sequential processing
- [ ] Progress tracking shows current label being printed (e.g., "150 of 200")
- [ ] Failed labels are retried automatically (up to 3 attempts)
- [ ] Partial print jobs can be resumed without reprinting successful labels
- [ ] Multiple concurrent batch jobs are handled without interference
- [ ] Job prioritization allows urgent jobs to jump queue
- [ ] Print queue status visible to users in real-time

## Queue Architecture

### Components
```
[Odoo] → [Flask API] → [Redis Queue] → [Worker] → [CUPS] → [Printer]
```

### Queue Tiers
1. **High Priority**: Urgent reprints, <10 labels
2. **Normal Priority**: Standard batch jobs, 10-200 labels  
3. **Low Priority**: Large batches >200 labels, test prints

## Technical Implementation

### Flask Queue Manager
```python
import redis
from rq import Queue

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
```

### Print Worker
```python
def process_batch_print(job_id, job_data):
    labels = job_data['labels']
    
    for idx, label in enumerate(labels, 1):
        # Update progress
        redis_conn.hset(f"job:{job_id}", 'current_label', idx)
        
        # Print with retry
        success = print_single_label(label, max_retries=3)
        
        if not success:
            redis_conn.rpush(f"job:{job_id}:failed", idx)
```

## Job Resume
```python
def resume_failed_job(job_id):
    failed_indices = redis_conn.lrange(f"job:{job_id}:failed", 0, -1)
    failed_labels = [original_labels[int(i)-1] for i in failed_indices]
    
    # Create new high-priority job for failed labels
    return enqueue_print_job({'labels': failed_labels}, priority='high')
```

## Performance
- Batch size limit: 200 labels recommended, 500 max
- Label print rate: ~100ms per label
- Concurrent jobs per printer: 2 max

## Related Documents
- [Flask API Component](../components/flask-api.md)
- [F01: Auto Print](F01-auto-print-on-mo-split.md)