from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.payment.register"

    check_date = fields.Date(string="Cheque Date")
    check_number = fields.Char(string="Cheque Number")
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        check_company=True,
        help="The account used for this payment.",
        store=True
    )
    tax_id = fields.Many2one(
        'account.tax',
        string='Tax',
        default=False,
        check_company=True,
        help="The tax used for this payment.",
        store=True
    )

    # Only for display, not persisted across save
    amount = fields.Monetary(
        currency_field='currency_id',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    taxed_amount = fields.Monetary(
        string='Taxed Amount',
        currency_field='currency_id',
        help="The amount of tax to be applied on the payment.",
        compute='_compute_taxed_amount',
        store=True,
        readonly=True
    )
    untaxed_amount = fields.Monetary(
        string='Untaxed Amount',
        currency_field='currency_id',
        help="The amount without tax to be applied on the payment.",
        compute='_compute_amount',
        store=True,
        readonly=True
    )

    # ---------- COMPUTES FOR DISPLAY IN THE FORM ----------

    @api.depends('tax_id', 'untaxed_amount', 'currency_id', 'partner_id')
    def _compute_taxed_amount(self):
        for record in self:
            if record.tax_id and record.untaxed_amount:
                tax_data = record.tax_id.compute_all(
                    record.untaxed_amount,
                    record.currency_id,
                    1,
                    partner=record.partner_id
                )
                record.taxed_amount = sum(t['amount'] for t in tax_data['taxes'])
            else:
                record.taxed_amount = 0.0
            _logger.info(
                "Compute Taxed Amount -> tax: %s, untaxed: %s, taxed: %s",
                record.tax_id, record.untaxed_amount, record.taxed_amount
            )

    @api.depends(
        'can_edit_wizard', 'source_amount', 'source_amount_currency',
        'source_currency_id', 'company_id', 'currency_id',
        'payment_date', 'installments_mode', 'tax_id'
    )
    def _compute_amount(self):
        for wizard in self:
            if not wizard.journal_id or not wizard.currency_id or not wizard.payment_date or wizard.custom_user_amount:
                wizard.amount = wizard.amount
            else:
                try:
                    total_amount_values = wizard._get_total_amounts_to_pay(wizard.batches) or {}
                except UserError:
                    wizard.amount = 0.0
                    wizard.untaxed_amount = 0.0
                    continue

                wizard.untaxed_amount = total_amount_values.get('amount_by_default', 0.0)

                if wizard.tax_id and wizard.untaxed_amount:
                    wizard.amount = wizard.untaxed_amount - wizard.taxed_amount
                else:
                    wizard.amount = wizard.untaxed_amount

            _logger.info("Compute Amount -> untaxed: %s, amount: %s",
                         wizard.untaxed_amount, wizard.amount)

    # ---------- MAIN PAYMENT CREATION ----------

    def _create_payment_vals_from_wizard(self, batch_result):
        self.ensure_one()

        # recompute amounts directly from batch_result (safe at save time)
        total_amount_values = self._get_total_amounts_to_pay(batch_result) or {}
        untaxed = total_amount_values.get('amount_by_default', 0.0)
        taxed = 0.0
        if self.tax_id and untaxed:
            tax_data = self.tax_id.compute_all(
                untaxed, self.currency_id, 1, partner=self.partner_id
            )
            taxed = sum(t['amount'] for t in tax_data['taxes'])

        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        payment_vals.update({
            "check_date": self.check_date,
            "check_number": self.check_number,
            "account_id": self.account_id.id if self.account_id else False,
            "tax_id": self.tax_id.id if self.tax_id else False,
            "taxed_amount": taxed,
            "untaxed_amount": untaxed,
        })

        _logger.info("Payment vals from wizard: %s", payment_vals)
        return payment_vals

    def _init_payments(self, to_process, edit_mode=False):
        payments = super()._init_payments(to_process, edit_mode=edit_mode)
        _logger.info("Payments created: %s", payments)
        for payment in payments:
            payment.check_date = self.check_date
            payment.check_number = self.check_number
            payment.account_id = self.account_id
            payment.tax_id = self.tax_id
        return payments


class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_date = fields.Date(string="Cheque Date", readonly=True)
    check_number = fields.Char(string="Cheque Number", readonly=True)
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        check_company=True,
        required=True,
        help="The account used for this payment.",
        store=True
    )
    tax_id = fields.Many2one(
        'account.tax',
        string='Tax',
        default=False,
        check_company=True,
        help="The tax used for this payment.",
        store=True
    )
    taxed_amount = fields.Monetary(
        string='Taxed Amount',
        currency_field='currency_id',
        help="The amount of tax to be applied on the payment.",
        store=True
    )
    untaxed_amount = fields.Monetary(
        string='Untaxed Amount',
        currency_field='currency_id',
        help="The amount without tax to be applied on the payment.",
        store=True
    )
