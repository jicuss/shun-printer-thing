"""Lot Number Generator Model

Complete model for generating and tracking unique lot numbers with collision
prevention and integration with stock tracking.

Source: F02-lot-number-generation.md - Example 9
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class LotNumberGenerator(models.Model):
    _name = 'lot.number.generator'
    _description = 'Lot Number Generation'
    
    mo_id = fields.Many2one('mrp.production', 'Manufacturing Order', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    lot_number = fields.Char('Lot Number', required=True, index=True)
    box_number = fields.Integer('Box Number')
    catch_weight = fields.Float('Catch Weight')
    label_printed = fields.Boolean('Label Printed', default=False)
    print_job_id = fields.Many2one('label.print.job', 'Print Job')
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)
    
    _sql_constraints = [
        ('lot_number_unique', 'UNIQUE(lot_number)', 
         'Lot number must be unique!')
    ]
    
    @api.model
    def generate_for_mo_split(self, mo, quantity):
        """Generate lot numbers for all units in MO split"""
        lot_records = []
        
        for i in range(quantity):
            lot_number = self._generate_unique_lot_number()
            
            lot_record = self.create({
                'mo_id': mo.id,
                'product_id': mo.product_id.id,
                'lot_number': lot_number,
                'box_number': i + 1,
                'catch_weight': self._get_catch_weight(mo, i),
            })
            lot_records.append(lot_record)
        
        return lot_records
    
    def _generate_unique_lot_number(self):
        """Generate unique lot number with collision prevention"""
        max_attempts = 10
        
        for attempt in range(max_attempts):
            lot_number = self.env['ir.sequence'].next_by_code(
                'lot.number.sequence'
            )
            
            # Check for collision (should be rare with proper sequence config)
            if not self.search([('lot_number', '=', lot_number)]):
                return lot_number
            
            _logger.warning(
                f"Lot number collision detected: {lot_number}. "
                f"Retry attempt {attempt + 1}/{max_attempts}"
            )
        
        raise ValidationError(
            "Unable to generate unique lot number after multiple attempts. "
            "Please contact system administrator."
        )
    
    def _get_catch_weight(self, mo, index):
        """Retrieve catch weight for specific product unit"""
        # Integration with existing catch weight module
        # This is read-only - we don't modify the catch weight module
        catch_weight_data = mo.move_raw_ids[index].catch_weight_info
        return catch_weight_data.weight if catch_weight_data else 0.0