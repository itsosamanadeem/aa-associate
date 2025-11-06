# models/account_move.py
from odoo import models, api, _, fields
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    total_professional_fees = fields.Monetary(
        currency_field="currency_id",
        string="Total Professional Fees",
        compute="_compute_professional_fees_total"
    )
    total_offical_fees = fields.Monetary(
        currency_field="currency_id",
        string="Total Official Fees",
        compute="_compute_offical_fees_total"
    )

    @api.depends('invoice_line_ids.offical_fees',
                 'invoice_line_ids.lenght_of_classes')
    def _compute_professional_fees_total(self):
        for rec in self:
            rec.total_professional_fees = sum(
                line.professional_fees * line.lenght_of_classes
                for line in rec.invoice_line_ids
            )

    @api.depends('invoice_line_ids.offical_fees',
                 'invoice_line_ids.lenght_of_classes')
    def _compute_offical_fees_total(self):
        for rec in self:
            rec.total_offical_fees = sum(
                line.offical_fees * line.lenght_of_classes
                for line in rec.invoice_line_ids
            )
