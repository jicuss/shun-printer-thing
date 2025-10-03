"""Flask API Unit Tests

Tests for Flask API endpoints including print job submission and error handling.

Source: operations/testing.md - Examples 40, 41 & 42
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_print_job_submission(client):
    """Test POST /api/print endpoint"""
    response = client.post('/api/print', json={
        'printer': 'zebra_z230_line1',
        'quantity': 1,
        'labels': [{'zpl_code': '^XA^FO50,50^A0N,50,50^FDTest^FS^XZ'}]
    }, headers={'Authorization': 'Bearer test-key'})
    
    assert response.status_code == 201
    assert 'job_id' in response.json


def test_invalid_printer(client):
    """Test submission to non-existent printer"""
    response = client.post('/api/print', json={
        'printer': 'invalid_printer',
        'quantity': 1,
        'labels': [{'zpl_code': '^XA^XZ'}]
    }, headers={'Authorization': 'Bearer test-key'})
    
    assert response.status_code == 404