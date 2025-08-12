# my_module/controllers/main.py
from odoo import http
from odoo.http import request

class ProductVariantController(http.Controller):

    @http.route('/get_product_variants', type='json', auth='public', methods=['POST'], csrf=False)
    def get_product_variants(self, product_tmpl_id):
        if not product_tmpl_id:
            return []
        product = request.env['product.product'].sudo().search([
            ('product_tmpl_id', '=', product_tmpl_id)
        ]).attribute_line_ids.mapped('value_ids')

        variants = request.env['product.template.attribute.value'].sudo().search([('attribute_id','in', product.ids)])

        return [
            {
                "name": v.name,
                "price": v.price_extra,
            }
            for v in variants
        ]
