# API Specification

## Base URL
```
https://print-server.local:5000/api
```

## Authentication
All requests require Bearer token authentication.

**Header**:
```
Authorization: Bearer {API_KEY}
```

## Endpoints

### 1. Submit Print Job

**Endpoint**: `POST /print`

**Description**: Submit a new print job with one or more labels

**Request Body**:
```json
{
  "printer": "string (required)",
  "quantity": "integer (required)",
  "labels": [
    {
      "zpl_code": "string (required)",
      "box_number": "integer (optional)",
      "lot_number": "string (optional)",
      "metadata": "object (optional)"
    }
  ],
  "job_metadata": {
    "mo_reference": "string (optional)",
    "priority": "string (optional: 'high', 'normal', 'low')"
  }
}
```

**Success Response** (201 Created):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "estimated_completion": "2025-10-02T15:30:00Z",
  "message": "Print job queued successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Printer not found
- `503 Service Unavailable`: Print service unavailable

---

### 2. Get Job Status

**Endpoint**: `GET /status/{job_id}`

**Description**: Retrieve current status of a print job

**Path Parameters**:
- `job_id` (required): UUID of the print job

**Success Response** (200 OK):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "printing",
  "progress": {
    "total": 200,
    "completed": 150,
    "failed": 0
  },
  "started_at": "2025-10-02T14:25:00Z",
  "estimated_completion": "2025-10-02T14:30:00Z",
  "printer": "zebra_z230_line1"
}
```

**Status Values**:
- `queued`: Job in queue, waiting to print
- `printing`: Currently printing
- `completed`: All labels printed successfully
- `failed`: Job failed
- `cancelled`: Job cancelled by user

**Error Response**:
- `404 Not Found`: Job ID not found

---

### 3. List Printers

**Endpoint**: `GET /printers`

**Description**: Get list of available printers and their status

**Success Response** (200 OK):
```json
{
  "printers": [
    {
      "name": "zebra_z230_line1",
      "model": "Zebra Z230",
      "status": "online",
      "connection": "USB",
      "location": "Production Line 1",
      "jobs_in_queue": 2
    }
  ]
}
```

---

### 4. Cancel Job

**Endpoint**: `DELETE /jobs/{job_id}`

**Description**: Cancel a queued or printing job

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "Job cancelled successfully"
}
```

**Error Response**:
- `404 Not Found`: Job not found
- `409 Conflict`: Job already completed, cannot cancel

---

### 5. Test Print

**Endpoint**: `POST /test`

**Description**: Send a test label to verify printer connectivity

**Request Body**:
```json
{
  "printer": "zebra_z230_line1"
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "Test label sent to printer"
}
```

---

### 6. Health Check

**Endpoint**: `GET /health`

**Description**: Check API and service health

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T14:30:00Z",
  "services": {
    "cups": "running",
    "redis": "connected",
    "workers": 2
  },
  "version": "1.0.0"
}
```

## Error Response Format

All error responses follow this structure:
```json
{
  "error": "Error title",
  "message": "Detailed error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-10-02T14:30:00Z"
}
```

## Rate Limiting

- **Limit**: 100 requests per minute per API key
- **Header**: `X-RateLimit-Remaining` indicates remaining requests
- **Response**: 429 Too Many Requests when limit exceeded

## Related Documents
- [Flask API Component](../components/flask-api.md)
- [System Architecture](../architecture/system-architecture.md)