#!/bin/bash
# Verify Deployment
#
# Checks that all containers are running and the API is responding.
#
# Source: operations/deployment.md - Example 60

# Check containers
sudo docker-compose ps

# Check logs
sudo docker-compose logs -f flask-api

# Test API
curl http://localhost:5000/api/health