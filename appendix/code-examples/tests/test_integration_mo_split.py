"""Integration Test: MO Split to Print

Tests complete flow from manufacturing order split to print job creation.

Source: operations/testing.md - Example 43
"""

from odoo.tests.common import TransactionCase


class TestMOSplitIntegration(TransactionCase):
    
    def test_mo_split_triggers_print(self):
        """Test complete flow from MO split to print job creation"""
        # Create MO
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 10
        })
        
        # Split MO
        mo.action_split_production()
        
        # Verify lot numbers generated
        lots = self.env['lot.number.generator'].search([('mo_id', '=', mo.id)])
        self.assertEqual(len(lots), 10)
        
        # Verify print job created
        print_job = self.env['label.print.job'].search([('mo_id', '=', mo.id)])
        self.assertTrue(print_job)
        self.assertEqual(print_job.quantity, 10)
        self.assertEqual(print_job.status, 'sent')