from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.payment.register"

    check_date = fields.Date(string="Cheque Date")
    check_number = fields.Char(string="Cheque Number")
    account_id = fields.Many2one('account.account', string='Account',required=True,check_company=True,help="The account used for this payment.", store=True)
    tax_id = fields.Many2one('account.tax', string='Tax',default=False,check_company=True, help="The tax used for this payment.", store=True)
    amount = fields.Monetary(currency_field='currency_id', store=True, readonly=True,compute='_compute_amount')
    taxed_amount = fields.Monetary(string='Taxed Amount', currency_field='currency_id', help="The amount of tax to be applied on the payment.", compute='_compute_taxed_amount', store=True, readonly=False)
    untaxed_amount = fields.Monetary(string='Untaxed Amount', currency_field='currency_id', help="The amount without tax to be applied on the payment.",compute='_compute_amount', store=True, readonly=False)

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
            _logger.info("Compute Taxed Amount -> tax: %s, untaxed: %s, taxed: %s", record.tax_id, record.untaxed_amount, record.taxed_amount)


            
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

                wizard.untaxed_amount = total_amount_values['amount_by_default'] or 0.0

                if wizard.tax_id and wizard.untaxed_amount:
                    wizard.amount = wizard.untaxed_amount - wizard.taxed_amount
                else:
                    wizard.amount = wizard.untaxed_amount
            _logger.info("Compute Amount -> untaxed: %s, amount: %s", wizard.untaxed_amount, wizard.amount)



    def _create_payment_vals_from_wizard(self, batch_result):
        for rec in self:
            rec._compute_amount()
            rec._compute_taxed_amount()
            payment_vals = super()._create_payment_vals_from_wizard(batch_result)
            payment_vals.update({
                "check_date": rec.check_date,
                "check_number": rec.check_number,
                "account_id": rec.account_id.id,
                "tax_id": rec.tax_id.id,
                "taxed_amount": rec.taxed_amount,
                "untaxed_amount": rec.untaxed_amount,
            })
            _logger.info("Payment vals from wizard: %s", payment_vals)

            return payment_vals
        

    def _init_payments(self, to_process, edit_mode=False):
        payments = super()._init_payments(to_process, edit_mode=edit_mode)

        # for payment, vals in zip(payments, to_process):
        #     tax_id = vals['create_vals'].get('tax_id')
        #     taxed_amount = vals['create_vals'].get('taxed_amount')
        #     account_id = vals['create_vals'].get('account_id')
        #     partner_id = vals['create_vals'].get('partner_id')
        #     communication = vals['create_vals'].get('communication', '')

        #     if tax_id and taxed_amount:
        #         payment.move_id.line_ids.create({
        #             'move_id': payment.move_id.id,
        #             'account_id': account_id,
        #             'partner_id': partner_id,
        #             'name': communication,
        #             'debit': taxed_amount,
        #             'credit': 0.0,
        #         })
        #         payment.move_id.line_ids.create({
        #             'move_id': payment.move_id.id,
        #             'account_id': self.env.ref('account.data_account_type_receivable').id,
        #             'partner_id': partner_id,
        #             'name': communication,
        #             'debit': 0.0,
        #             'credit': taxed_amount,
        #         })

        # _logger.info("Payment vals to process: %s", to_process)
        return payments



class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_date = fields.Date(string="Cheque Date", readonly=True,)
    check_number = fields.Char(string="Cheque Number",readonly=True,)
    account_id = fields.Many2one('account.account', string='Account',check_company=True,required=True, help="The account used for this payment.", store=True)
    tax_id = fields.Many2one('account.tax', string='Tax',default=False,check_company=True, help="The tax used for this payment.", store=True)
    taxed_amount = fields.Monetary(string='Taxed Amount', currency_field='currency_id', help="The amount of tax to be applied on the payment.",check_company=True,store=True,)
    untaxed_amount = fields.Monetary(string='Untaxed Amount', currency_field='currency_id', help="The amount without tax to be applied on the payment.",check_company=True,store=True,)
    