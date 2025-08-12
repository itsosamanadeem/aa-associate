from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductAttributeInvoiceWizard(models.TransientModel):
    _name = "product.attribute.invoice.wizard"
    _description = "Invoice Line Product Configurator"

    invoice_line_id = fields.Many2one('account.move.line', required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True,)
    product_tmpl_id = fields.Many2one('product.template', required=True)
    # attribute_id = fields.Many2one('product.template.attribute.line', string="Attribute", required=True)
    attribute_value_ids = fields.One2many(
        comodel_name='product.template.attribute.value', 
        inverse_name="attribute_id",
        compute='_compute_attribute_values',
        string="Attributes",
        store=True, readonly=False, precompute=True, copy=True)

    @api.depends('product_tmpl_id')
    def _compute_attribute_values(self):
        for rec in self:
            if rec.product_tmpl_id:
                attribute_ids = rec.product_tmpl_id.attribute_line_ids.mapped('attribute_id').ids
                variants = rec.env['product.template.attribute.value'].search([
                    ('attribute_id', 'in', attribute_ids)
                ])
                rec.attribute_value_ids = variants
            else:
                rec.attribute_value_ids = False

    def action_confirm(self):
        self.ensure_one()
        # Find variant for selected attribute values

        # product_variant = self.product_tmpl_id._get_variant_for_combination(self.attribute_value_ids)
        raise UserError(_("Please select at least one attribute value.")) if not self.attribute_value_ids else None
        if not product_variant:
            raise UserError("No product variant matches the selected attributes.")
        self.invoice_line_id.product_id = product_variant.id
        return {'type': 'ir.actions.act_window_close'}
