"""Integration Test: Odoo-Flask Communication

Tests Odoo successfully calls Flask API with mocked responses.

Source: operations/testing.md - Example 44
"""

import responses
from odoo.tests.common import TransactionCase


class TestOdooFlaskIntegration(TransactionCase):
    
    @responses.activate
    def test_flask_api_communication(self):
        """Test Odoo successfully calls Flask API"""
        # Mock Flask API response
        responses.add(
            responses.POST,
            'https://print-server.local:5000/api/print',
            json={'job_id': 'test-uuid', 'status': 'queued'},
            status=201
        )
        
        job = self.env['label.print.job'].create({
            'mo_id': self.mo.id,
            'quantity': 5,
            'status': 'pending',
            'labels_data': '[]'
        })
        job._submit_to_print_server()
        
        # Verify job updated with Flask job ID
        self.assertEqual(job.flask_job_id, 'test-uuid')
        self.assertEqual(job.status, 'sent')