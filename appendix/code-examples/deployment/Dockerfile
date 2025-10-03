# Docker Container for Flask Print Server
#
# Builds a containerized Flask application with CUPS integration.
#
# Source: operations/deployment.md - Example 57

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libcups2-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]