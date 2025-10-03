"""MO Split Detection and Label Printing Trigger

This module extends the Manufacturing Order (MRP) model to detect split events
and automatically trigger label printing workflows.

Source: F01-auto-print-on-mo-split.md - Examples 1 & 2
"""

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def action_split_production(self):
        """Override split action to trigger label printing"""
        result = super().action_split_production()
        
        # Trigger automatic label generation
        if self.env.context.get('auto_print_labels', True):
            self._trigger_label_printing()
        
        return result
    
    def _trigger_label_printing(self):
        """Initiate automatic label print workflow"""
        LabelPrintJob = self.env['label.print.job']
        LabelPrintJob.create_from_mo_split(self)