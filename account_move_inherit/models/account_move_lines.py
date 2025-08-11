# models/account_move_line.py
from odoo import models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _onchange_product_id_open_wizard(self):
        if self.product_id and self.product_id.product_tmpl_id.attribute_line_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Configure Product',
                'res_model': 'product.attribute.invoice.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_invoice_line_id': self.id,
                    'default_product_tmpl_id': self.product_id.product_tmpl_id.id,
                }
            }
