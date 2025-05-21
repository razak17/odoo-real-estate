from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    property_id = fields.Many2one('property')

    def action_confirm(self):
        print("hello inside action_confirm")

        return super(SaleOrder,self).action_confirm()


