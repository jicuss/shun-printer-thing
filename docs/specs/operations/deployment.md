# Deployment Guide

## Overview
Step-by-step guide for deploying the shun-printer label printing system.

## Prerequisites

### Hardware
- Ubuntu Server 20.04 LTS or newer
- Minimum 2GB RAM, 20GB disk space
- Zebra Z230 printer (300 DPI)
- Network connectivity to Odoo server
- Static IP address for print server

### Accounts & Access
- Odoo admin account
- Ubuntu server sudo access
- Printer on same network (or USB connected)

## Deployment Steps

### Phase 1: Ubuntu Server Setup

**1. Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

**2. Install Dependencies**
```bash
# Docker
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# CUPS
sudo apt install cups cups-client -y
sudo systemctl start cups
sudo systemctl enable cups

# Python dependencies
sudo apt install python3-pip python3-cups -y
```

**3. Configure Firewall**
```bash
# Allow Flask API port
sudo ufw allow 5000/tcp

# Allow CUPS web interface (optional)
sudo ufw allow 631/tcp

# Enable firewall
sudo ufw enable
```

**4. Set Static IP** (if not already configured)
```bash
# Edit netplan config
sudo nano /etc/netplan/01-netcfg.yaml
```

Example config:
```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Apply:
```bash
sudo netplan apply
```

---

### Phase 2: Printer Configuration

**1. Connect Zebra Z230**
- USB: Plug in and verify with `lsusb`
- Network: Ensure printer has static IP

**2. Add Printer to CUPS**

```bash
# USB connection
sudo lpadmin -p zebra_z230_line1 \
  -E \
  -v usb://Zebra%20Technologies/ZTC%20ZD230-203dpi%20ZPL \
  -m raw

# Network connection
sudo lpadmin -p zebra_z230_line1 \
  -E \
  -v socket://192.168.1.200:9100 \
  -m raw

# Set as default
sudo lpadmin -d zebra_z230_line1
```

**3. Test Printer**
```bash
echo "^XA^FO50,50^A0N,50,50^FDTest Print^FS^XZ" | lp -d zebra_z230_line1 -o raw
```

---

### Phase 3: Flask Server Deployment

**1. Clone/Copy Application**
```bash
cd /opt
sudo mkdir label-print-server
cd label-print-server
```

**2. Create Directory Structure**
```
label-print-server/
├── app.py
├── worker.py
├── requirements.txt
├── .env
├── Dockerfile
├── docker-compose.yml
└── logs/
```

**3. Create requirements.txt**
```txt
Flask==2.3.3
gunicorn==21.2.0
python-cups==2.0.1
redis==5.0.0
rq==1.15.1
requests==2.31.0
python-dotenv==1.0.0
```

**4. Create .env File**
```bash
API_KEY=your-secret-api-key-here
REDIS_HOST=localhost
REDIS_PORT=6379
LOG_LEVEL=INFO
```

**5. Create Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libcups2-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**6. Create docker-compose.yml**
```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

  flask-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - /var/run/cups/cups.sock:/var/run/cups/cups.sock
    depends_on:
      - redis
    restart: unless-stopped

  worker:
    build: .
    command: rq worker print --url redis://redis:6379
    environment:
      - REDIS_HOST=redis
    env_file:
      - .env
    volumes:
      - /var/run/cups/cups.sock:/var/run/cups/cups.sock
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis-data:
```

**7. Deploy with Docker Compose**
```bash
sudo docker-compose up -d
```

**8. Verify Deployment**
```bash
# Check containers
sudo docker-compose ps

# Check logs
sudo docker-compose logs -f flask-api

# Test API
curl http://localhost:5000/api/health
```

---

### Phase 4: Odoo Module Installation

**1. Upload Module**
- Package module as ZIP: `label_print.zip`
- Upload via Odoo Apps menu (if using custom modules)
- Or copy to addons directory (self-hosted Odoo)

**2. Update Apps List**
```
Settings → Apps → Update Apps List
```

**3. Install Module**
- Search: "Label Print - Catch Weight"
- Click Install

**4. Configure System Parameters**

Navigate to: `Settings → Technical → Parameters → System Parameters`

Add:
```
label_print.api_url = https://192.168.1.100:5000
label_print.api_key = your-secret-api-key-here
label_print.default_printer = zebra_z230_line1
```

**5. Import Default Template**

Navigate to: `Manufacturing → Configuration → Label Templates`

- Import provided template or create new
- Set as default template
- Assign to product categories

**6. Configure Printer**

Navigate to: `Manufacturing → Configuration → Printers`

- Name: Zebra Z230 Line 1
- CUPS Name: zebra_z230_line1
- IP: 192.168.1.200 (if network)
- DPI: 300
- Set as default: Yes

---

### Phase 5: Testing

**1. Create Test MO**
- Product: Any catch weight product
- Quantity: 5 units

**2. Split MO**
- Split into 5 units
- Verify labels print automatically

**3. Test Manual Reprint**
- Open completed MO
- Click "Reprint Labels"
- Select range: Boxes 2-3
- Verify only 2 labels print

**4. Verify Print Job History**
- Navigate to print job dashboard
- Verify job logged with correct status

---

### Phase 6: Production Rollout

**1. User Training**
- Train commissary staff on reprint function
- Provide quick reference guide

**2. Monitor Initial Usage**
- Watch print job success rate
- Check error logs for issues

**3. Adjust as Needed**
- Fine-tune label templates
- Optimize printer settings

## Post-Deployment

### Backup Configuration
```bash
# Backup Odoo database
# (via Odoo database manager)

# Backup Flask server config
sudo tar -czf label-print-backup.tar.gz /opt/label-print-server
```

### Set Up Monitoring
- Configure log rotation
- Set up alerting for print failures
- Monitor server resources

## Troubleshooting

See [Maintenance Guide](maintenance.md) for common issues and solutions.

## Related Documents
- [System Architecture](../architecture/system-architecture.md)
- [Maintenance Guide](maintenance.md)
- [Testing Guide](testing.md)