"""GS1-128 Barcode Generator

Generates GS1-128 compliant barcode data strings for catch weight products,
including proper weight encoding and date formatting.

Source: F03-gs1-barcode-creation.md - Example 13
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GS1BarcodeGenerator(models.AbstractModel):
    _name = 'gs1.barcode.generator'
    
    @api.model
    def generate_gs1_data_string(self, product, lot_number, catch_weight, 
                                  production_date=None, expiration_date=None):
        """Generate complete GS1-128 data string"""
        
        gtin = self._format_gtin(product.barcode)
        lot = lot_number
        weight = self._encode_weight(catch_weight, decimal_places=3)
        prod_date = self._format_date(production_date or fields.Date.today())
        
        data_string = f"(01){gtin}(10){lot}(3103){weight}(11){prod_date}"
        
        if expiration_date:
            exp_date = self._format_date(expiration_date)
            data_string += f"(17){exp_date}"
        
        self._validate_gs1_data_string(data_string)
        return data_string
    
    def _format_gtin(self, barcode):
        if not barcode:
            raise ValidationError("Product must have a barcode/GTIN")
        gtin = ''.join(filter(str.isdigit, barcode))
        return gtin.zfill(14)
    
    def _encode_weight(self, weight, decimal_places=3):
        multiplier = 10 ** decimal_places
        weight_int = int(round(weight * multiplier))
        return str(weight_int).zfill(6)
    
    def _format_date(self, date):
        if isinstance(date, str):
            date = fields.Date.from_string(date)
        return date.strftime('%y%m%d')