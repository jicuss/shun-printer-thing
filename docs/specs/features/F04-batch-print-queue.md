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

> **Code Example**: See [appendix/code-examples/flask/queue_manager.py](../../../appendix/code-examples/flask/queue_manager.py)

Manages print job queuing with three priority tiers (high, normal, low) using Redis and RQ for reliable batch processing.

### Print Worker

> **Code Example**: See [appendix/code-examples/flask/print_worker.py](../../../appendix/code-examples/flask/print_worker.py)

RQ worker that processes batches sequentially, tracks progress in Redis, and maintains a list of failed labels for retry.

## Job Resume

> **Code Example**: See [appendix/code-examples/flask/job_resume.py](../../../appendix/code-examples/flask/job_resume.py)

Retrieves failed label indices from Redis and creates a new high-priority job to reprint only the failed labels.

## Performance
- Batch size limit: 200 labels recommended, 500 max
- Label print rate: ~100ms per label
- Concurrent jobs per printer: 2 max

## Related Documents
- [Flask API Component](../components/flask-api.md)
- [F01: Auto Print](F01-auto-print-on-mo-split.md)