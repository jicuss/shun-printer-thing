#!/bin/bash
# Clear Print Queue
#
# Cancels all jobs in the print queue.
#
# Source: components/cups-printer.md - Example 80

cancel -a zebra_z230_line1
sudo systemctl restart cups