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

> **Script**: See [appendix/code-examples/deployment/01-system-update.sh](../../../appendix/code-examples/deployment/01-system-update.sh)

**2. Install Dependencies**

> **Script**: See [appendix/code-examples/deployment/02-install-dependencies.sh](../../../appendix/code-examples/deployment/02-install-dependencies.sh)

**3. Configure Firewall**

> **Script**: See [appendix/code-examples/deployment/03-configure-firewall.sh](../../../appendix/code-examples/deployment/03-configure-firewall.sh)

**4. Set Static IP** (if not already configured)
```bash
# Edit netplan config
sudo nano /etc/netplan/01-netcfg.yaml
```

Example config:

> **Config File**: See [appendix/code-examples/deployment/netplan-config.yaml](../../../appendix/code-examples/deployment/netplan-config.yaml)

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

> **Scripts**: 
> - USB: [appendix/code-examples/deployment/04-add-printer-usb.sh](../../../appendix/code-examples/deployment/04-add-printer-usb.sh)
> - Network: [appendix/code-examples/deployment/05-add-printer-network.sh](../../../appendix/code-examples/deployment/05-add-printer-network.sh)

**3. Test Printer**

> **Script**: See [appendix/code-examples/deployment/06-test-printer.sh](../../../appendix/code-examples/deployment/06-test-printer.sh)

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

> **File**: See [appendix/code-examples/deployment/requirements.txt](../../../appendix/code-examples/deployment/requirements.txt)

**4. Create .env File**

> **Template**: See [appendix/code-examples/deployment/.env.example](../../../appendix/code-examples/deployment/.env.example)

**5. Create Dockerfile**

> **File**: See [appendix/code-examples/deployment/Dockerfile](../../../appendix/code-examples/deployment/Dockerfile)

**6. Create docker-compose.yml**

> **File**: See [appendix/code-examples/deployment/docker-compose.yml](../../../appendix/code-examples/deployment/docker-compose.yml)

**7. Deploy with Docker Compose**

> **Script**: See [appendix/code-examples/deployment/07-deploy-docker.sh](../../../appendix/code-examples/deployment/07-deploy-docker.sh)

**8. Verify Deployment**

> **Script**: See [appendix/code-examples/deployment/08-verify-deployment.sh](../../../appendix/code-examples/deployment/08-verify-deployment.sh)

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

> **Script**: See [appendix/code-examples/deployment/backup-config.sh](../../../appendix/code-examples/deployment/backup-config.sh)

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