"""Lot Number Quick Search

Provides quick lookup functionality for traceability queries.

Source: F02-lot-number-generation.md - Example 12
"""

from odoo import models


class LotNumberGenerator(models.Model):
    _inherit = 'lot.number.generator'
    
    def search_by_lot_number(self, lot_number):
        """Quick lookup by lot number for traceability"""
        return self.search([('lot_number', '=', lot_number)])