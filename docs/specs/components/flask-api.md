# Flask API Component

## Overview
REST API service that receives print jobs from Odoo, manages print queue, and interfaces with CUPS to send ZPL data to Zebra printers.

## Technology Stack
- **Framework**: Flask 2.3+ or FastAPI 0.100+
- **Queue**: Redis + RQ (Redis Queue)
- **WSGI Server**: Gunicorn
- **Deployment**: Docker container

## API Endpoints

### POST /api/print
Submit new print job

**Request**:
```json
{
  "printer": "zebra_z230_line1",
  "quantity": 200,
  "labels": [
    {
      "zpl_code": "^XA...^XZ",
      "box_number": 1,
      "lot_number": "LOT-2025-000001"
    }
  ],
  "job_metadata": {
    "mo_reference": "MO/2025/001",
    "priority": "normal"
  }
}
```

**Response** (201 Created):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "estimated_completion": "2025-10-02T15:30:00Z"
}
```

### GET /api/status/{job_id}
Get job status

**Response** (200 OK):
```json
{
  "job_id": "550e8400...",
  "status": "printing",
  "progress": {
    "total": 200,
    "completed": 150,
    "failed": 0
  },
  "started_at": "2025-10-02T14:25:00Z",
  "estimated_completion": "2025-10-02T14:30:00Z"
}
```

### GET /api/printers
List available printers

**Response** (200 OK):
```json
{
  "printers": [
    {
      "name": "zebra_z230_line1",
      "model": "Zebra Z230",
      "status": "online",
      "connection": "USB",
      "jobs_in_queue": 2
    }
  ]
}
```

### POST /api/test
Send test print

**Request**:
```json
{
  "printer": "zebra_z230_line1"
}
```

### GET /api/health
Health check

**Response** (200 OK):
```json
{
  "status": "healthy",
  "cups": "running",
  "redis": "connected",
  "workers": 2
}
```

## Implementation

### Main Application

```python
# app.py
from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import cups
import uuid

app = Flask(__name__)
redis_conn = Redis(host='localhost', port=6379)
print_queue = Queue('print', connection=redis_conn)

@app.route('/api/print', methods=['POST'])
def submit_print_job():
    # Validate API key
    if not validate_api_key(request.headers.get('Authorization')):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # Validate request
    if not data.get('printer') or not data.get('labels'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Enqueue job
    job = print_queue.enqueue(
        'worker.process_print_job',
        job_id,
        data,
        job_timeout='30m'
    )
    
    # Store job metadata
    redis_conn.hmset(f"job:{job_id}", {
        'status': 'queued',
        'quantity': data['quantity'],
        'printer': data['printer']
    })
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'estimated_completion': estimate_completion(data['quantity'])
    }), 201

@app.route('/api/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job_data = redis_conn.hgetall(f"job:{job_id}")
    
    if not job_data:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({
        'job_id': job_id,
        'status': job_data.get(b'status').decode(),
        'progress': {
            'total': int(job_data.get(b'quantity', 0)),
            'completed': int(job_data.get(b'current_label', 0)),
            'failed': 0
        }
    }), 200

def validate_api_key(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    token = auth_header.split(' ')[1]
    return token == os.getenv('API_KEY')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Print Worker

```python
# worker.py
import cups
import time
from redis import Redis

redis_conn = Redis(host='localhost', port=6379)

def process_print_job(job_id, job_data):
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
            
            # Print via CUPS
            print_label(conn, printer_name, label['zpl_code'])
            
            time.sleep(0.1)  # Prevent printer overload
        
        # Mark complete
        redis_conn.hset(f"job:{job_id}", 'status', 'completed')
        
    except Exception as e:
        redis_conn.hset(f"job:{job_id}", 'status', 'failed')
        redis_conn.hset(f"job:{job_id}", 'error', str(e))
        raise

def print_label(conn, printer, zpl_code):
    # Send raw ZPL to printer
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(zpl_code)
        temp_path = f.name
    
    try:
        conn.printFile(printer, temp_path, "Label", {'raw': 'true'})
    finally:
        os.unlink(temp_path)
```

## Authentication

### API Key Method
```python
API_KEY = os.getenv('API_KEY', 'your-secret-key-here')

def validate_api_key(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    return auth_header.split(' ')[1] == API_KEY
```

## Error Handling

```python
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server error: {error}')
    return jsonify({'error': 'Internal server error'}), 500
```

## Logging

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/flask.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=10
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[handler]
)
```

## Related Documents
- [System Architecture](../architecture/system-architecture.md)
- [API Specification](../reference/api-spec.md)
- [Deployment Guide](../operations/deployment.md)