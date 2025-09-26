# models/account_payment_register.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.payment.register"

    check_date = fields.Date(string="Cheque Date")
    check_number = fields.Char(string="Cheque Number")
    account_id = fields.Many2one(
        'account.account', string='Account', check_company=True,
        help="The account used for this payment.", store=True
    )
    tax_id = fields.Many2one(
        'account.tax', string='Tax', default=False, check_company=True,
        help="The tax used for this payment.", store=True
    )

    amount = fields.Monetary(
        currency_field='currency_id', store=True, readonly=True, compute='_compute_amount'
    )
    taxed_amount = fields.Monetary(
        string='Taxed Amount', currency_field='currency_id',
        help="The tax amount for this payment.", compute='_compute_taxed_amount',
        store=True, readonly=True
    )
    untaxed_amount = fields.Monetary(
        string='Untaxed Amount', currency_field='currency_id',
        help="The amount before tax.", compute='_compute_amount',
        store=True, readonly=True
    )

    @api.depends('tax_id')
    def _compute_taxed_amount(self):
        for rec in self:
            if rec.tax_id and rec.untaxed_amount:
                tax_data = rec.tax_id.compute_all(
                    rec.untaxed_amount,
                    rec.currency_id,
                    1,
                    partner=rec.partner_id
                )
                rec.taxed_amount = sum(t.get('amount', 0.0) for t in tax_data.get('taxes', []))
            else:
                rec.taxed_amount = 0.0

    @api.depends(
        'can_edit_wizard', 'source_amount', 'source_amount_currency',
        'source_currency_id', 'company_id', 'currency_id',
        'payment_date', 'installments_mode', 'taxed_amount',
    )
    def _compute_amount(self):
        for wizard in self:
            # Basic guards (wizard not ready)
            if not wizard.journal_id or not wizard.currency_id or not wizard.payment_date or wizard.custom_user_amount:
                # keep existing values (avoid forcing zeros during initialization)
                wizard.amount = wizard.amount or 0.0
                wizard.untaxed_amount = wizard.untaxed_amount or 0.0
                wizard.taxed_amount = wizard.taxed_amount or 0.0
                continue

            # Try to compute totals from batches; if the core raises UserError
            # (happens during registry loading / upgrade), fallback to zeros.
            try:
                total_amount_values = (wizard._get_total_amounts_to_pay(wizard.batches) or {})
            except UserError:
                wizard.amount = 0.0
                wizard.untaxed_amount = 0.0
                wizard.taxed_amount = 0.0
                continue

            base = total_amount_values.get('amount_by_default') or total_amount_values.get('full_amount') or 0.0
            wizard.untaxed_amount = base

            if wizard.tax_id and base:
                tax_data = wizard.tax_id.compute_all(base, wizard.currency_id, 1, partner=wizard.partner_id)
                taxed = sum(t.get('amount', 0.0) for t in tax_data.get('taxes', []))
                wizard.taxed_amount = taxed
                # set gross amount = untaxed + taxed
                wizard.amount = base + taxed
            else:
                wizard.taxed_amount = 0.0
                wizard.amount = base

    def _create_payment_vals_from_wizard(self, batch_result):
        """
        Build final vals for account.payment. IMPORTANT: compute amounts from batch_result
        (not only rely on wizard cached fields), then inject them into the returned vals.
        """
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)

        # Determine base amount robustly from batch_result
        base_amount = 0.0
        try:
            if isinstance(batch_result, dict):
                base_amount = (
                    batch_result.get('amount_by_default')
                    or batch_result.get('full_amount')
                    or batch_result.get('amount')
                    or 0.0
                )

                # If batch_result contains move lines and base_amount is still 0, sum residuals
                lines = batch_result.get('lines') or batch_result.get('move_lines') or []
                if not base_amount and lines:
                    # lines may be a recordset or a list - handle both
                    if hasattr(lines, 'mapped'):
                        base_amount = sum(lines.mapped('amount_residual') or lines.mapped('balance') or [])
                    else:
                        # fallback for plain lists of objects/dicts
                        try:
                            base_amount = sum(
                                (getattr(l, 'amount_residual', 0.0) or l.get('amount_residual', 0.0)
                                 or getattr(l, 'balance', 0.0) or l.get('balance', 0.0)
                                ) for l in lines
                            )
                        except Exception:
                            base_amount = 0.0
            else:
                # batch_result is not dict (older/newer variants) — use wizard cache
                base_amount = self.untaxed_amount or 0.0
        except Exception:
            base_amount = self.untaxed_amount or 0.0

        # Compute taxed amount using chosen tax and currency
        taxed = 0.0
        if self.tax_id and base_amount:
            try:
                tax_data = self.tax_id.compute_all(base_amount, self.currency_id, 1, partner=self.partner_id)
                taxed = sum(t.get('amount', 0.0) for t in tax_data.get('taxes', []))
            except Exception:
                taxed = 0.0

        untaxed = base_amount
        gross = untaxed + taxed

        # Inject guaranteed amounts and other custom fields into payment vals
        payment_vals.update({
            "untaxed_amount": untaxed or 0.0,
            "taxed_amount": taxed or 0.0,
            # override amount (gross) if you want gross; if you prefer net, change to untaxed
            "amount": gross or payment_vals.get('amount', 0.0),
            "check_date": self.check_date,
            "check_number": self.check_number,
            "account_id": self.account_id.id or False,
            "tax_id": self.tax_id.id or False,
        })

        return payment_vals


class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_date = fields.Date(string="Cheque Date", readonly=True)
    check_number = fields.Char(string="Cheque Number", readonly=True)
    account_id = fields.Many2one(
        'account.account', string='Account', check_company=True,
        # make optional unless you need it mandatory for all payments
        required=False, help="The account used for this payment.", store=True
    )
    tax_id = fields.Many2one(
        'account.tax', string='Tax', default=False, check_company=True,
        help="The tax used for this payment.", store=True
    )
    taxed_amount = fields.Monetary(
        string='Taxed Amount', currency_field='currency_id',
        help="The amount of tax to be applied on the payment.", store=True
    )
    untaxed_amount = fields.Monetary(
        string='Untaxed Amount', currency_field='currency_id',
        help="The amount without tax to be applied on the payment.", store=True
    )
