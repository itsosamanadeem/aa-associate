# my_module/controllers/main.py
from odoo import http
from odoo.http import request

class ProductVariantController(http.Controller):

    @http.route('/get_product_variants', type='json', auth='public', methods=['POST'], csrf=False)
    def get_product_variants(self, product_tmpl_id):
        if not product_tmpl_id:
            return []
        variants = request.env['product.product'].sudo().search([
            ('product_tmpl_id', '=', product_tmpl_id)
        ])
        return [
            {
                "id": v.id,
                "name": v.display_name,
                "default_code": v.default_code or "",
                "price": v.list_price,
            }
            for v in variants
        ]
