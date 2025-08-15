# models/account_move_line.py
from odoo import models, api, _, fields
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_template_id = fields.Many2one(
        string="Product Template",
        comodel_name='product.template',
        compute='_compute_product_template_id',
        readonly=False,
        search='_search_product_template_id',
        domain=[('sale_ok', '=', True)]
    )

    # Store exactly what the dialog shows: PTAVs
    selected_ptav_ids = fields.Many2many(
        'product.template.attribute.value',
        string="Selected Variant Values",
        help="Attribute values selected for this line."
    )

    @api.depends('product_id')
    def _compute_product_template_id(self):
        for line in self:
            line.product_template_id = line.product_id.product_tmpl_id

    def _search_product_template_id(self, operator, value):
        return [('product_id.product_tmpl_id', operator, value)]

    def update_price_unit(self, vals):
        """Update price_unit and selected PTAVs for this line."""
        self.ensure_one()
        price = vals.get("price")
        if price is None:
            raise UserError(_("No price provided"))

        try:
            price = float(price)
        except Exception:
            raise UserError(_("Invalid price value"))

        # write price
        self.price_unit = price

        # write selected PTAVs (overwrite)
        if "selected_ptav_ids" in vals:
            self.write({
                "selected_ptav_ids": [(6, 0, vals["selected_ptav_ids"])]
            })

        return {"status": "success", "new_price_unit": self.price_unit}
