# models/account_move_line.py
from odoo import models, api, _ , fields
from odoo.exceptions import UserError
import json

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    product_template_id = fields.Many2one(
        string="Product Variants",
        comodel_name='product.template',
        compute='_compute_product_template_id',
        readonly=False,
        search='_search_product_template_id',
        domain=[('sale_ok', '=', True)])

    selected_variant_ids = fields.Json(
        string='Selected Variants',
    )
    selected_variant_names = fields.Json(string="Variant Names")
    
    trademark_id = fields.Many2one(
        comodel_name="res.partner.trademark",
        string="Trademark",
        domain="[('partner_id', '=', parent.partner_id)]",
    )

    @api.depends('product_id')
    def _compute_product_template_id(self):
        for line in self:
            line.product_template_id = line.product_id.product_tmpl_id

    def _search_product_template_id(self, operator, value):
        return [('product_id.product_tmpl_id', operator, value)]

    def update_price_unit(self, vals):
        """ Update price_subtotal of this account.move.line """
        self.ensure_one()  # Only one line at a time
        price = vals.get("price")
        variants = vals.get("selected_variant_ids",[])
        variants_names = vals.get("selected_variant_names",[])

        if price is None:
            raise UserError(_("No price provided"))

        try:
            price = float(price)
        except ValueError:
            raise UserError(_("Invalid price value"))

        self.price_unit = price
        self.selected_variant_ids = variants
        self.selected_variant_names = variants_names
        return {"status": "success", "new_price_subtotal": self.price_subtotal}
