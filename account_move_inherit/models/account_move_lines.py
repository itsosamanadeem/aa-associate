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

    trademark_id = fields.Selection(
        selection=lambda self: self.trademark_name_selection(),
        string="Trademark",
    )

    @api.model
    def trademark_name_selection(self):
        partner = self.env['res.partner'].browse(self.move_id.partner_id)
        raise UserError(_("Partner: %s" % partner))
        if not partner:
            return []
        return [
            (str(trademark.id), trademark.x_studio_trademark_name)
            for trademark in partner
        ]


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

        # raise UserError(_(f"{variants}"))
        if price is None:
            raise UserError(_("No price provided"))

        # Ensure numeric
        try:
            price = float(price)
        except ValueError:
            raise UserError(_("Invalid price value"))

        self.price_unit = price
        # if variants:
        self.selected_variant_ids = variants
        self.selected_variant_names = variants_names
        # raise UserError(_(f"Updated price: {self.price_unit} with variants: {self.selected_variant_ids} variant names: {self.selected_variant_names}"))
        return {"status": "success", "new_price_subtotal": self.price_subtotal}
