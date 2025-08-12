# controllers/wizard_controller.py
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class WizardController(http.Controller):

    @http.route('/open_variant_price_wizard', type='json', auth='user', methods=['POST'], csrf=False)
    def open_variant_price_wizard(self, product_id):
        product = request.env['product.product'].browse(product_id)
        raise UserError(product)
        if not product.exists():
            return False  # JS should handle this

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.variant.price.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': product.id,
                'active_model': 'product.product',
            }
        }

