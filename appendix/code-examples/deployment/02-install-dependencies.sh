#!/bin/bash
# Install System Dependencies
#
# Installs Docker, CUPS, and Python dependencies required for the print server.
#
# Source: operations/deployment.md - Example 49

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