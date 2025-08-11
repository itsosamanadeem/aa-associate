# models/account_move_line.py
from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_attribute_wizard(self):
        line = self.invoice_line_ids.filtered(lambda l: l.product_id and l.product_id.product_tmpl_id.attribute_line_ids)[:1]
        if not line:
            return
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configure Product',
            'res_model': 'product.attribute.invoice.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': line.product_id.id,
                'default_invoice_line_id': line.id,
            }
        }
