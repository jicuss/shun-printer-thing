#!/bin/bash
# Install CUPS and Python CUPS Bindings
#
# Installs CUPS print system and python-cups library.
#
# Source: components/cups-printer.md - Example 71

# Install CUPS
sudo apt update
sudo apt install cups cups-client

# Install python-cups
pip install pycups

# Start CUPS service
sudo systemctl start cups
sudo systemctl enable cups