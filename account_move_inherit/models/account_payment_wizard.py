from odoo import fields, models, api, _
from odoo.exceptions import UserError

class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.payment.register"

    check_date = fields.Date(string="Cheque Date")
    check_number = fields.Char(string="Cheque Number")
    account_id = fields.Many2one('account.account', string='Account',check_company=True,help="The account used for this payment.", store=True)
    tax_id = fields.Many2one('account.tax', string='Tax',default=False,check_company=True, help="The tax used for this payment.", store=True)
    # tax = fields.Float(string='Tax Rate (%)', help="The tax rate to be applied on the payment.", default=0.0)
    amount = fields.Monetary(currency_field='currency_id', store=True, readonly=True,compute='_compute_amount')
    taxed_amount = fields.Monetary(string='Taxed Amount', currency_field='currency_id', help="The amount of tax to be applied on the payment.", compute='_compute_taxed_amount', store=True, readonly=True)
    untaxed_amount = fields.Monetary(string='Untaxed Amount', currency_field='currency_id', help="The amount without tax to be applied on the payment.",compute='_compute_amount', store=True)

    @api.depends('untaxed_amount', 'tax_id')
    def _compute_taxed_amount(self):
        for record in self:
            if record.tax_id and record.untaxed_amount:
                tax_data = record.tax_id.compute_all(record.untaxed_amount, record.currency_id, 1, partner=record.partner_id)
                record.taxed_amount = sum(t['amount'] for t in tax_data['taxes'])
            else:
                record.taxed_amount = 0.0

    
    @api.depends(
        'can_edit_wizard', 'source_amount', 'source_amount_currency',
        'source_currency_id', 'company_id', 'currency_id',
        'payment_date', 'installments_mode', 'tax_id'
    )
    def _compute_amount(self):
        for wizard in self:
            if not wizard.journal_id or not wizard.currency_id or not wizard.payment_date or wizard.custom_user_amount:
                wizard.amount = wizard.amount or 0.0
                wizard.untaxed_amount = wizard.untaxed_amount or 0.0
            else:
                total_amount_values = wizard._get_total_amounts_to_pay(wizard.batches) or {}
                base_amount = total_amount_values.get('amount_by_default', 0.0)

                # Untaxed amount = full amount from Odoo
                wizard.untaxed_amount = total_amount_values.get('full_amount', base_amount)

                # Apply tax if selected
                if wizard.tax_id:
                    tax_data = wizard.tax_id.compute_all(base_amount, wizard.currency_id, 1, partner=wizard.partner_id)
                    tax_amount = sum(t['amount'] for t in tax_data['taxes'])
                    wizard.amount = base_amount - tax_amount
                else:
                    wizard.amount = base_amount


    def _get_total_amounts_to_pay(self, batch_results):
        rec = super()._get_total_amounts_to_pay(batch_results)
        if not rec:
            rec = {"amount_by_default": 0.0, "full_amount": 0.0}
        rec.update({
            "untaxed_amount": rec.get('full_amount', 0.0),
            "taxed_amount": self.taxed_amount,
        })
        return rec

    def _create_payment_vals_from_wizard(self, batch_result):
        """Extend to add check fields into created payments"""
        vals_list = super()._create_payment_vals_from_wizard(batch_result)
        vals_list.update({
            "check_date": self.check_date,
            "check_number": self.check_number,
            "account_id": self.account_id.id,
            "tax_id": self.tax_id.id,
            "taxed_amount": self.taxed_amount,
            "untaxed_amount": self.untaxed_amount,
        })
        return vals_list

class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_date = fields.Date(string="Cheque Date", readonly=True,)
    check_number = fields.Char(string="Cheque Number",readonly=True,)
    account_id = fields.Many2one('account.account', string='Account',check_company=True,required=True, help="The account used for this payment.", store=True)
    tax_id = fields.Many2one('account.tax', string='Tax',default=False,check_company=True, help="The tax used for this payment.", store=True)
    taxed_amount = fields.Monetary(string='Taxed Amount', currency_field='currency_id', help="The amount of tax to be applied on the payment.",check_company=True,)
    untaxed_amount = fields.Monetary(string='Untaxed Amount', currency_field='currency_id', help="The amount without tax to be applied on the payment.",check_company=True,)
    

    # tax = fields.Float(string='Tax Rate (%)', help="The tax rate to be applied on the payment.", default=0.0)
