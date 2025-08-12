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
