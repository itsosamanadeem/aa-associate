# models/account_move_line.py
from odoo import models, api, _ , fields
from odoo.exceptions import UserError
import json
from odoo.tools import format_date

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Description of service',
        inverse='_inverse_product_id',
        ondelete='restrict',
        check_company=True,
    )
    extra_flags = fields.Json("Extra Flags", default=dict)
    
    product_template_id = fields.Many2one(
        string="Classes",
        comodel_name='product.template',
        compute='_compute_product_template_id',
        search='_search_product_template_id',
        )
    attachment_name = fields.Char(string="Filename")
    logo_attachment_id = fields.Binary(string="Logo",help="Upload Logo of the required service!!!")
    country_id = fields.Many2one(string="Country", comodel_name='res.country', help="Country for which this logo is available")
    city_selection = fields.Selection(
        selection=[
            ('lahore', 'Lahore'),
            ('karachi', 'Karachi'),
            ('islamabad', 'Islamabad'),
        ],
        string="City",
    )
    opposition_number = fields.Json(
        string="Opposition Number",
        help="Stores mapping of classes → input value",
        store=True
    )
    appeal_number = fields.Json(
        string="Appeal Number",
        help="Stores mapping of classes → input value",
        store=True
    )
    suit_number = fields.Json(
        string="Suit Number",
        help="Stores mapping of classes → input value",
        store=True
    )
    filing_date= fields.Date(String="Filing Date")
    rectification_no = fields.Json(
        string="Rectification Number",
        help="Stores mapping of classes → input value",
        store=True
    )
    registration_no =fields.Json(
        string="Registration Number",
        help="Stores mapping of classes → input value",
        store=True
    )
    application_variant_data = fields.Json(
        string="Application Number",
        help="Stores mapping of classes → input value",
        store=True
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

    @api.onchange('move_id.partner_id', 'product_id', 'trademark_id')
    def _onchange_partner_id_and_product_id(self):
        """ Update the price_unit based on Trademark History (fee_per_class) """
        self.ensure_one()
        if self.move_id.partner_id and self.product_id and self.trademark_id:
            history_line = self.move_id.partner_id.trademark_history_ids.filtered(
                lambda h: h.services_taken == self.product_id and h.trademark_id == self.trademark_id and self.product_id.name == "Professional Fees"
            )
            if history_line:
                self.price_unit = history_line.fee_per_class
            else:
                self.price_unit = 0.0


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
        # application_number = vals.get("application_numbers", {})

        if price is None:
            raise UserError(_("No price provided"))

        try:
            price = float(price)
        except ValueError:
            raise UserError(_("Invalid price value"))

        self.price_unit = price
        self.selected_variant_ids = variants
        self.selected_variant_names = variants_names
        # self.application_id = application_number  
        # raise UserError(_("Application Number: %s") % self.application_id)
        return {"status": "success", "new_price_subtotal": self.price_subtotal}
    
    def get_field_label(self, field_name):
        field = self._fields.get(field_name)
        if field:
            return field.string
        return field_name

    def get_field_value(self, field_name):
        """Return a display-ready value for a given field name"""
        field = self._fields.get(field_name)
        if not field:
            return ""

        value = getattr(self, field_name, False)
        if not value:
            return ""

        # Handle Many2one
        if field.type == "many2one":
            if field.name == "trademark_id" and value:
                return value.trademark_name
            if field.name == "product_template_id" and self.selected_variant_names:
                return ", ".join(self.selected_variant_names or [])
            return value.display_name

        # Handle Date / Datetime
        if field.type == "date":
            return format_date(self.env, value)
        if field.type == "datetime":
            return fields.Datetime.to_string(value)

        # Handle Binary (image/logo)
        if field.type == "binary":
            # raise UserError(value)
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            mimetype = "image/png"  # default
            if hasattr(self, "logo_attachment_id") and self.attachment_name:
                if self.attachment_name.lower().endswith(".jpg") or self.attachment_name.lower().endswith(".jpeg"):
                    mimetype = "image/jpeg"
                elif self.attachment_name.lower().endswith(".gif"):
                    mimetype = "image/gif"
                elif self.attachment_name.lower().endswith(".svg"):
                    mimetype = "image/svg+xml"
            return f"data:{mimetype};base64,{value}"

        # Handle Dict
        if isinstance(value, dict):
            return ", ".join(f"{k}: {v}" for k, v in value.items())

        # Handle List/Tuple
        if isinstance(value, (list, tuple)):
            return ", ".join(str(v) for v in value)

        # Default fallback
        return str(value)

