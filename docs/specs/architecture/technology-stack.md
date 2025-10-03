# Technology Stack

## Platform

### Odoo ERP
- **Type**: SaaS (Cloud-hosted)
- **Version**: Latest stable (14.0+ recommended)
- **Database**: PostgreSQL (managed by Odoo)
- **Hosting**: Odoo.com or Odoo.sh

## Programming Languages

### Python
- **Version**: 3.8+
- **Usage**: 
  - Odoo custom module development
  - Flask print server
  - CUPS integration

### JavaScript
- **Usage**: Odoo web client UI enhancements
- **Framework**: Odoo's OWL (Owl Web Library) or legacy JS

### ZPL (Zebra Programming Language)
- **Version**: ZPL II
- **Usage**: Label template definition
- **DPI**: 300 (Zebra Z230 native resolution)

## Odoo Module Stack

### Core Dependencies
- **odoo**: Base framework
- **mrp**: Manufacturing (MRP) module
- **stock**: Inventory/warehouse management
- **product**: Product master data

### Python Libraries
- **requests**: HTTP client for Flask API calls
- **python-barcode** or **treepoem**: GS1-128 barcode generation
- **jinja2**: Template rendering (if needed beyond Odoo's QWeb)

## Flask Print Server Stack

### Web Framework
- **Flask** (recommended) or **FastAPI**
- **Version**: Flask 2.3+ or FastAPI 0.100+

### Key Libraries
- **flask** / **fastapi**: Web framework
- **python-cups**: CUPS integration (pycups)
- **redis** or **rq**: Job queue (optional but recommended)
- **requests**: HTTP client for callbacks
- **python-dotenv**: Environment variable management
- **gunicorn** or **uvicorn**: WSGI/ASGI server

### Data Storage
- **Redis**: Job queue and status cache (optional)
- **SQLite**: Job history and configuration (alternative to Redis)

## Infrastructure

### Operating System
- **Ubuntu Server**: 20.04 LTS or 22.04 LTS
- **Minimum Requirements**:
  - 2GB RAM
  - 20GB disk space
  - Static IP address

### Containerization
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### Print Management
- **CUPS** (Common Unix Printing System): 2.3+
- **Zebra Printer Drivers**: Raw/passthrough mode (no driver processing)

## Hardware

### Printer
- **Model**: Zebra Z230
- **Resolution**: 300 DPI
- **Protocol**: ZPL II
- **Connectivity**: USB or Network (Ethernet)
- **Print Method**: Direct thermal

## External Services

### Labelary.com
- **Purpose**: ZPL preview and validation
- **API**: REST API (free tier available)
- **Endpoint**: `http://api.labelary.com/v1/printers/{dpi}dpmm/labels/{width}x{height}/0/`
- **Usage**: Template preview in Odoo admin UI

## Security

### SSL/TLS
- **Let's Encrypt**: Free SSL certificates (recommended)
- **Self-signed**: Alternative for internal networks

### Authentication
- **API Key**: Simple bearer token authentication
- **Alternative**: JWT tokens for more complex setups

## Development Tools

### Recommended
- **VS Code** or **PyCharm**: IDE
- **Git**: Version control
- **Postman** or **curl**: API testing
- **ZebraDesigner**: ZPL template design (optional)

## Deployment Architecture

```
┌────────────────────────┐
│   Odoo Cloud (SaaS)      │
│   - Python 3.8+          │
│   - PostgreSQL           │
│   - Custom Module        │
└────────────────────────┘
         │ HTTPS
         ▼
┌────────────────────────┐
│ Ubuntu Server 20.04+   │
│                        │
│ ┌────────────────────┐ │
│ │ Docker Container   │ │
│ │                    │ │
│ │ Flask 2.3+         │ │
│ │ + Gunicorn         │ │
│ │ + Redis (optional) │ │
│ └────────────────────┘ │
│                        │
│ CUPS 2.3+              │
└────────────────────────┘
         │ USB/Network
         ▼
┌────────────────────────┐
│   Zebra Z230 (300DPI)   │
└────────────────────────┘
```

## Library Versions (Recommended)

### Odoo Module
```python
# No requirements.txt - dependencies managed by Odoo
# Declare in __manifest__.py:
'depends': ['mrp', 'stock', 'product']
```

### Flask Server
```txt
Flask==2.3.3
gunicorn==21.2.0
python-cups==2.0.1
redis==5.0.0
rq==1.15.1
requests==2.31.0
python-dotenv==1.0.0
```

## Related Documents
- [System Architecture](system-architecture.md)
- [Flask API Component](../components/flask-api.md)
- [Deployment Guide](../operations/deployment.md)