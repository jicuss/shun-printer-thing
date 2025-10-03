"""Unit Tests for GS1 Barcode Generation

Tests for weight encoding and GTIN validation.

Source: operations/testing.md - Examples 38 & 39
"""

from odoo.tests.common import TransactionCase


class TestGS1Barcode(TransactionCase):
    
    def test_weight_encoding(self):
        """Test catch weight encoding"""
        generator = self.env['gs1.barcode.generator']
        
        # Test 1.250 kg
        encoded = generator._encode_weight(1.250, decimal_places=3)
        self.assertEqual(encoded, '001250')
        
        # Test edge cases
        encoded = generator._encode_weight(0.001, decimal_places=3)
        self.assertEqual(encoded, '000001')
        
        encoded = generator._encode_weight(999.999, decimal_places=3)
        self.assertEqual(encoded, '999999')
    
    def test_gtin_validation(self):
        """Test GTIN check digit validation"""
        generator = self.env['gs1.barcode.generator']
        
        # Valid GTIN
        self.assertTrue(generator._validate_gtin_check_digit('00012345678905'))
        
        # Invalid GTIN
        self.assertFalse(generator._validate_gtin_check_digit('00012345678904'))