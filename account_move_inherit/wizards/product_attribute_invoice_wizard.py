from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductAttributeInvoiceWizard(models.TransientModel):
    _name = "product.attribute.invoice.wizard"
    _description = "Invoice Line Product Configurator"

    invoice_line_id = fields.Many2one('account.move.line', required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_tmpl_id = fields.Many2one('product.template', required=True)

    attribute_line_ids = fields.One2many(
        'product.attribute.invoice.wizard.line',
        'wizard_id',
        string="Attributes"
    )

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        if self.product_tmpl_id:
            attribute_ids = self.product_tmpl_id.attribute_line_ids.mapped('attribute_id').ids
            variants = self.env['product.template.attribute.value'].search([
                ('attribute_id', 'in', attribute_ids)
            ])
            self.attribute_line_ids = [
                (0, 0, {'attribute_value_id': v.id}) for v in variants
            ]
        else:
            self.attribute_line_ids = [(5, 0, 0)]

    def action_confirm(self):
        pass
        # self.ensure_one()
        # # Find variant for selected attribute values

        # # product_variant = self.product_tmpl_id._get_variant_for_combination(self.attribute_value_ids)
        # raise UserError(_("Please select at least one attribute value.")) if not self.attribute_value_ids else None
        # if not product_variant:
        #     raise UserError("No product variant matches the selected attributes.")
        # self.invoice_line_id.product_id = product_variant.id
        # return {'type': 'ir.actions.act_window_close'}
