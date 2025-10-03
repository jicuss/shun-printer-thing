"""Lot Number Format Validation

Validates lot number format using regex constraints to ensure consistency.

Source: F02-lot-number-generation.md - Example 11
"""

import re
from odoo import models, api
from odoo.exceptions import ValidationError


class LotNumberGenerator(models.Model):
    _inherit = 'lot.number.generator'
    
    @api.constrains('lot_number')
    def _check_lot_number_format(self):
        """Validate lot number matches expected format"""
        pattern = r'^LOT-\d{4}-\d{6}$'
        for record in self:
            if not re.match(pattern, record.lot_number):
                raise ValidationError(
                    f"Invalid lot number format: {record.lot_number}. "
                    f"Expected format: LOT-YYYY-NNNNNN"
                )