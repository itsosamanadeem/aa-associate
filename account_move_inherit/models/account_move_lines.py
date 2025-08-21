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
        search='_search_product_template_id',
        )

    selected_variant_ids = fields.Json(
        string='Selected Variants',
    )
    selected_variant_names = fields.Json(string="Variant Names")
    
    trademark_id = fields.Many2one(
        comodel_name="res.partner.trademark",
        string="Trademark",
        domain="[('partner_id', '=', parent.partner_id)]",
    )


    @api.onchange('move_id.partner_id','product_id')
    def _onchange_partner_id_and_product_id(self):
        """ Update the trademark_id based on the partner and product selection """
        self.ensure_one()
        if self.move_id.partner_id:
            price_list= self.move_id.partner_id.property_product_pricelist.item_ids
            if not price_list:
                raise UserError(_("No price list items found for the selected partner."))
            
            if self.product_id.product_tmpl_id in price_list.mapped('product_tmpl_id'):
                self.price_unit = price_list.filtered(
                    lambda item: item.product_tmpl_id == self.product_id.product_tmpl_id
                ).price
    
    # @api.onchange('trademark_id')
    # def _onchange_trademark_id(self):
    #     self.ensure_one()
    #     if not self.trademark_id:
    #         self.price_unit = 0.0
    #     if self.trademark_id:
    #         self.price_unit = self.trademark_id.trademark_price

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
