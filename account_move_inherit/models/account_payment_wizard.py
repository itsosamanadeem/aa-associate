from odoo import fields, models, api, _
from odoo.exceptions import UserError

class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.payment.register"

    check_date = fields.Date(string="Cheque Date")
    check_number = fields.Char(string="Cheque Number")
    account_id = fields.Many2one('account.account', string='Account', check_company=True)
    tax_id = fields.Many2one('account.tax', string='Tax', check_company=True)
    taxed_amount = fields.Monetary(string='Taxed Amount', currency_field='currency_id')
    untaxed_amount = fields.Monetary(string='Untaxed Amount', currency_field='currency_id')

    def _create_payment_vals_from_wizard(self, batch_result):
        """Force custom values into account.payment vals."""
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)

        # --- compute untaxed + tax safely ---
        base = batch_result.get("amount", 0.0) if isinstance(batch_result, dict) else 0.0
        untaxed = base
        taxed = 0.0
        if self.tax_id and untaxed:
            tax_data = self.tax_id.compute_all(untaxed, self.currency_id, 1, partner=self.partner_id)
            taxed = sum(t["amount"] for t in tax_data.get("taxes", []))

        # --- inject custom vals ---
        payment_vals.update({
            "check_date": self.check_date,
            "check_number": self.check_number,
            "account_id": self.account_id.id,
            "tax_id": self.tax_id.id,
            "untaxed_amount": untaxed,
            "taxed_amount": taxed,
            "amount": untaxed - taxed,   # force gross
        })

        return payment_vals


class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_date = fields.Date(string="Cheque Date", readonly=True)
    check_number = fields.Char(string="Cheque Number", readonly=True)
    account_id = fields.Many2one('account.account', string='Account', check_company=True, store=True)
    tax_id = fields.Many2one('account.tax', string='Tax', check_company=True, store=True)
    taxed_amount = fields.Monetary(string="Taxed Amount", currency_field="currency_id", store=True)
    untaxed_amount = fields.Monetary(string="Untaxed Amount", currency_field="currency_id", store=True)
