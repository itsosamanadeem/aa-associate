# my_module/controllers/main.py
from odoo import http
from odoo.http import request

class ProductVariantController(http.Controller):

    @http.route('/open_product_variants', type='json', auth='user')
    def open_product_variants(self, product_tmpl_id):
        if not product_tmpl_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "name": "Product Variants",
            "res_model": "product.product",
            "view_mode": "tree,form",
            "domain": [("product_tmpl_id", "=", product_tmpl_id)],
            "target": "new",  # opens in a dialog
            "context": {"default_product_tmpl_id": product_tmpl_id},
        }
