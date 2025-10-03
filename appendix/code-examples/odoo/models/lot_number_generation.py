"""Lot Number Generation Logic

Simple lot number generation for MO splits. This is used within the print job
creation workflow.

Source: F01-auto-print-on-mo-split.md - Example 3
"""

from odoo import fields


def _generate_lot_numbers(self, mo_id, quantity):
    """Generate sequential lot numbers for MO split"""
    year = fields.Date.today().year
    base_sequence = self.env['ir.sequence'].next_by_code('lot.number.sequence')
    
    lot_numbers = []
    for i in range(quantity):
        lot_number = f"LOT-{year}-{base_sequence + i:06d}"
        lot_numbers.append(lot_number)
    
    return lot_numbers