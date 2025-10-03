#!/bin/bash
# Fix CUPS Permissions
#
# Adds user to lpadmin group for printer management.
#
# Source: components/cups-printer.md - Example 79

sudo usermod -a -G lpadmin $USER