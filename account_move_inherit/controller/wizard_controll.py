# my_module/controllers/main.py
from odoo import http
from odoo.http import request
import json

class ProductVariantController(http.Controller):

    @http.route('/get_product_variants', type='json', auth='public', methods=['POST'], csrf=False)
    def get_product_variants(self, product_tmpl_id, line_id=None):
        if not product_tmpl_id:
            return []

        products = request.env['product.product'].sudo().search([
            ('product_tmpl_id', '=', product_tmpl_id)
        ])
        product_detail = products.attribute_line_ids.mapped('attribute_id').ids
        variants = request.env['product.template.attribute.value'].sudo().search([
            ('attribute_id', 'in', product_detail)
        ])

        # get previously saved variant IDs if line_id is passed
        selected_ids = []
        if line_id:
            move_line = request.env['account.move.line'].sudo().browse(line_id)
            if move_line.exists() and move_line.selected_variant_ids:
                try:
                    # stored as JSON string
                    selected_ids = json.loads(move_line.selected_variant_ids)
                except Exception:
                    pass

        return [
            {   
                "product_image": products[0].image_1920 if products else None,
                'product_id': products[0].id if products else None,
                'product_name': products[0].name if products else None,
                'id': v.id,
                "name": v.name,
                "price": v.price_extra,
                "is_selected": v.id in selected_ids,  # ✅ mark selected
            }
            for v in variants
        ]
