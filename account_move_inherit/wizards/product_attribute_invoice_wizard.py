# models/product_attribute_invoice_wizard.py
from odoo import models, fields

class ProductAttributeInvoiceWizard(models.TransientModel):
    _name = "product.attribute.invoice.wizard"
    _description = "Invoice Line Product Configurator"

    invoice_line_id = fields.Many2one('account.move.line', required=True)
    product_tmpl_id = fields.Many2one('product.template', required=True)
    attribute_value_ids = fields.Many2many(
        'product.template.attribute.line',
        string="Attributes"
    )

    def action_confirm(self):
        product_variant = self.product_tmpl_id._get_variant_for_combination(
            self.attribute_value_ids
        )
        if product_variant:
            self.invoice_line_id.product_id = product_variant.id
        return {'type': 'ir.actions.act_window_close'}
