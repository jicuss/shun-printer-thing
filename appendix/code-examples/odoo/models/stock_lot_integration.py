"""Stock Production Lot Integration

Creates Odoo stock.production.lot records for full traceability integration
with the standard inventory system.

Source: F02-lot-number-generation.md - Example 10
"""

from odoo import models


class LotNumberGenerator(models.Model):
    _inherit = 'lot.number.generator'
    
    def _create_stock_production_lot(self):
        """Create Odoo stock.production.lot records for traceability"""
        StockLot = self.env['stock.production.lot']
        
        for lot_gen in self:
            StockLot.create({
                'name': lot_gen.lot_number,
                'product_id': lot_gen.product_id.id,
                'company_id': lot_gen.mo_id.company_id.id,
                'ref': f"MO: {lot_gen.mo_id.name} - Box {lot_gen.box_number}"
            })