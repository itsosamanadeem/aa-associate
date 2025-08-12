from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductAttributeInvoiceWizardLine(models.TransientModel):
    _name = "product.attribute.invoice.wizard.line"
    _description = "Wizard Line for Attribute Selection"

    wizard_id = fields.Many2one('product.attribute.invoice.wizard', required=True, ondelete='cascade')
    attribute_value_id = fields.Many2one('product.template.attribute.value', required=True)
    is_selected = fields.Boolean("Selected")
