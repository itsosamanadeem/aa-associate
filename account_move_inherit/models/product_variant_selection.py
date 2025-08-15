# models/product_variant_selection.py
from odoo import models, fields

class ProductVariantSelection(models.Model):
    _name = 'product.variant.selection'
    _description = 'Product Variant Selection'

    move_line_id = fields.Many2one('account.move.line', required=True, ondelete='cascade')
    variant_id = fields.Many2one('product.product', required=True)
    variant_name = fields.Char(related="variant_id.name", store=True)
    is_selected = fields.Boolean(default=False)
