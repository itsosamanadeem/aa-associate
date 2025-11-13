# models/account_move.py
from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    total_professional_fees = fields.Monetary(
        currency_field="currency_id",
        string="Total Professional Fees",
        compute="_compute_professional_fees_total"
    )
    total_official_fees = fields.Monetary(
        currency_field="currency_id",
        string="Total Official Fees",
        compute="_compute_official_fees_total"
    )

    @api.depends('invoice_line_ids.professional_fees',
                 'invoice_line_ids.lenght_of_classes')
    def _compute_professional_fees_total(self):
        for rec in self:
            total = 0
            for line in rec.invoice_line_ids:
                if line.lenght_of_classes:
                    total += line.professional_fees * line.lenght_of_classes
                else:
                    total += line.professional_fees
            rec.total_professional_fees = total

    @api.depends('invoice_line_ids.official_fees',
                 'invoice_line_ids.lenght_of_classes')
    def _compute_official_fees_total(self):
        for rec in self:
            total = 0
            for line in rec.invoice_line_ids:
                if line.lenght_of_classes:
                    total += line.official_fees * line.lenght_of_classes
                else:
                    total += line.official_fees
            rec.total_official_fees = total
