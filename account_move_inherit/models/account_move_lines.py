# models/account_move_line.py
from odoo import models, api, _ , fields
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move.line'


    product_template_id = fields.Many2one(
        string="Product Template",
        comodel_name='product.template',
        compute='_compute_product_template_id',
        readonly=False,
        search='_search_product_template_id',
        domain=[('sale_ok', '=', True)])


    @api.depends('product_id')
    def _compute_product_template_id(self):
        for line in self:
            line.product_template_id = line.product_id.product_tmpl_id

    def _search_product_template_id(self, operator, value):
        return [('product_id.product_tmpl_id', operator, value)]
    
class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_attribute_wizard(self):
        # Find first invoice line with a product having variants
        line = self.invoice_line_ids.filtered(lambda l: l.product_id and l.product_id.product_tmpl_id.attribute_line_ids)[:1]
        if not line:
            raise UserError("Please select a product with variants to configure.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configure Product Variants',
            'res_model': 'product.attribute.invoice.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_line_id': line.id,
                'default_product_tmpl_id': line.product_id.product_tmpl_id.id,
            },
        }
