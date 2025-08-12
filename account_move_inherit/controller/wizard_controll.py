# controllers/wizard_controller.py
from odoo import http
from odoo.http import request

class WizardController(http.Controller):

    @http.route('/open_variant_price_wizard', type='json', auth='public', methods=['POST'], csrf=False)
    def open_variant_price_wizard(self, product_id):

        line_id= request.env['account.move.line'].browse(product_id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.variant.price.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': product_id,
                'active_model': 'account.move.line',
            }
        }
