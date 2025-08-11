from odoo import models, fields, api
from odoo.exceptions import UserError
class ProductAttributeInvoiceWizard(models.TransientModel):
    _name = "product.attribute.invoice.wizard"
    _description = "Invoice Line Product Configurator"

    invoice_line_id = fields.Many2one('account.move.line', required=True)
    product_tmpl_id = fields.Many2one('product.template', required=True)
    attribute_value_ids = fields.Many2many(
        'product.attribute.value',
        string="Attributes"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        invoice_line = self.env['account.move.line'].browse(res.get('invoice_line_id'))
        if invoice_line and invoice_line.product_id:
            # Pre-fill the product template and selected attribute values of current variant
            res['product_tmpl_id'] = invoice_line.product_id.product_tmpl_id.id
            res['attribute_value_ids'] = [(6, 0, invoice_line.product_id.attribute_value_ids.ids)]
        return res

    def action_confirm(self):
        self.ensure_one()
        # Find variant for selected attribute values
        product_variant = self.product_tmpl_id._get_variant_for_combination(self.attribute_value_ids)
        if not product_variant:
            raise UserError("No product variant matches the selected attributes.")
        self.invoice_line_id.product_id = product_variant.id
        return {'type': 'ir.actions.act_window_close'}
