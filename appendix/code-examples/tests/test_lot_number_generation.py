"""Unit Tests for Lot Number Generation

Tests for lot number uniqueness and sequential numbering.

Source: operations/testing.md - Examples 36 & 37
"""

from odoo.tests.common import TransactionCase


class TestLotNumberGeneration(TransactionCase):
    
    def test_unique_lot_numbers(self):
        """Verify lot numbers are unique"""
        mo = self.env.ref('mrp.test_mo')
        generator = self.env['lot.number.generator']
        
        lots = generator.generate_for_mo_split(mo, quantity=10)
        lot_numbers = [lot.lot_number for lot in lots]
        
        # All unique
        self.assertEqual(len(lot_numbers), len(set(lot_numbers)))
    
    def test_sequential_numbering(self):
        """Verify lot numbers are sequential"""
        mo = self.env.ref('mrp.test_mo')
        generator = self.env['lot.number.generator']
        
        lots = generator.generate_for_mo_split(mo, quantity=5)
        
        # Extract sequence numbers
        sequences = [int(lot.lot_number.split('-')[-1]) for lot in lots]
        
        # Check sequential
        for i in range(1, len(sequences)):
            self.assertEqual(sequences[i], sequences[i-1] + 1)