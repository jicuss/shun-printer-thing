# Maintenance Guide

## Overview
Ongoing maintenance procedures, monitoring, troubleshooting, and system updates.

## Daily Checklist

```bash
# Check services
sudo docker-compose ps
systemctl status cups
lpstat -p zebra_z230_line1

# Check logs
sudo tail -50 /opt/label-print-server/logs/flask.log | grep -i error

# Check disk space
df -h
```

## Monitoring

### Key Metrics
- Print success rate: >95%
- API response time: <500ms
- Queue time: <2 min
- Disk usage: <80%

### Log Locations
- Flask: `/opt/label-print-server/logs/flask.log`
- CUPS: `/var/log/cups/error_log`
- Docker: `sudo docker-compose logs`

## Troubleshooting

### Printer Offline

**Symptoms**: Print jobs fail, CUPS shows stopped

**Resolution**:
```bash
# Check connection
ping 192.168.1.200

# Resume printer
sudo cupsenable zebra_z230_line1

# Test print
echo "^XA^FO50,50^A0N,50,50^FDTest^FS^XZ" | lp -d zebra_z230_line1 -o raw
```

### Flask Server Unresponsive

**Symptoms**: API timeout, jobs stuck

**Resolution**:
```bash
# Restart containers
sudo docker-compose restart

# Check health
curl http://localhost:5000/api/health

# Check logs
sudo docker-compose logs --tail=100
```

### Barcodes Not Scanning

**Resolution**:
- Increase barcode height in template
- Clean printer head
- Adjust printer darkness: `echo "^XA^SD15^XZ" | lp -d zebra_z230_line1 -o raw`
- Verify FNC1 characters in GS1 data

## Backup

### Daily Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/backup/label-print"
DATE=$(date +%Y%m%d)

# Backup config
sudo tar -czf "$BACKUP_DIR/config-$DATE.tar.gz" /opt/label-print-server

# Backup Redis
sudo docker-compose exec redis redis-cli SAVE

# Clean old backups (30 days)
find "$BACKUP_DIR" -mtime +30 -delete
```

## Updates

### Flask Server Update
```bash
cd /opt/label-print-server
sudo git pull
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d
```

### System Updates
```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart docker
```

## Performance Tuning

### Scale Workers
```bash
# Increase Flask workers
sudo docker-compose up -d --scale worker=6
```

### CUPS Optimization
Edit `/etc/cups/cupsd.conf`:
```
MaxJobs 500
JobRetryLimit 5
```

## Preventive Maintenance

### Weekly
- Review error logs
- Check disk space
- Verify backups
- Test printer

### Monthly
- Clean printer head
- Review performance
- Update documentation
- Archive old jobs

### Quarterly
- Full backup test
- Security audit
- User training
- Capacity planning

## Emergency Recovery

```bash
# Stop services
sudo docker-compose down

# Restore from backup
sudo tar -xzf /backup/config-latest.tar.gz -C /

# Restart
sudo docker-compose up -d

# Verify
curl http://localhost:5000/api/health
```

## Support Contacts

| Issue | Contact | Response |
|-------|---------|----------|
| Printer | Zebra Support | 4 hours |
| Odoo | Odoo Support | 24 hours |
| System | Internal IT | 2 hours |
| Urgent | On-call Admin | 30 min |

## Related Documents
- [Deployment Guide](deployment.md)
- [Testing Guide](testing.md)