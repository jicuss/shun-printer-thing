# Maintenance Guide

## Overview
Ongoing maintenance procedures, monitoring, troubleshooting, and system updates.

## Daily Checklist

> **Script**: See [appendix/code-examples/maintenance/daily-checklist.sh](../../../appendix/code-examples/maintenance/daily-checklist.sh)

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

> **Script**: See [appendix/code-examples/maintenance/fix-printer-offline.sh](../../../appendix/code-examples/maintenance/fix-printer-offline.sh)

### Flask Server Unresponsive

**Symptoms**: API timeout, jobs stuck

**Resolution**:

> **Script**: See [appendix/code-examples/maintenance/restart-flask.sh](../../../appendix/code-examples/maintenance/restart-flask.sh)

### Barcodes Not Scanning

**Resolution**:
- Increase barcode height in template
- Clean printer head
- Adjust printer darkness: `echo "^XA^SD15^XZ" | lp -d zebra_z230_line1 -o raw`
- Verify FNC1 characters in GS1 data

## Backup

### Daily Backup Script

> **Script**: See [appendix/code-examples/maintenance/daily-backup.sh](../../../appendix/code-examples/maintenance/daily-backup.sh)

## Updates

### Flask Server Update

> **Script**: See [appendix/code-examples/maintenance/update-flask.sh](../../../appendix/code-examples/maintenance/update-flask.sh)

### System Updates

> **Script**: See [appendix/code-examples/maintenance/system-update.sh](../../../appendix/code-examples/maintenance/system-update.sh)

## Performance Tuning

### Scale Workers

> **Script**: See [appendix/code-examples/maintenance/scale-workers.sh](../../../appendix/code-examples/maintenance/scale-workers.sh)

### CUPS Optimization

> **Config**: See [appendix/code-examples/maintenance/cups-optimization.conf](../../../appendix/code-examples/maintenance/cups-optimization.conf)

Edit `/etc/cups/cupsd.conf` and add these settings.

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

> **Script**: See [appendix/code-examples/maintenance/emergency-recovery.sh](../../../appendix/code-examples/maintenance/emergency-recovery.sh)

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