# models/account_move.py
from odoo import models, api, _, fields
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"


    total_professional_fees = fields.Monetary(currency_field="currency_id",string="Total Professional Fees", compute="compute_professional_fees_total")
    total_offical_fees = fields.Monetary(currency_field="currency_id",string="Total Offical Fees")

    @api.depends('invoice_line_ids.professional_fees','invoice_line_ids.offical_fees','invoice_line_ids.lenght_of_classes')
    def compute_professional_fees_total(self):
        for rec in self:
            raise UserError(rec.invoice_line_ids.professional_fees)
        

# class AccountTax(models.Model):
#     _inherit = "account.tax"
    
#     @api.model
#     def _prepare_base_line_for_taxes_computation(self, record, **kwargs):
#         """ Convert any representation of a business object ('record') into a base line being a python
#         dictionary that will be used to use the generic helpers for the taxes computation.

#         The whole method is designed to ease the conversion from a business record.
#         For example, when passing either account.move.line, either sale.order.line or purchase.order.line,
#         providing explicitely a 'product_id' in kwargs is not necessary since all those records already have
#         an `product_id` field.

#         :param record:  A representation of a business object a.k.a a record or a dictionary.
#         :param kwargs:  The extra values to override some values that will be taken from the record.
#         :return:        A dictionary representing a base line.
#         """
#         def load(field, fallback):
#             return self._get_base_line_field_value_from_record(record, field, kwargs, fallback)

#         currency = (
#             load('currency_id', None)
#             or load('company_currency_id', None)
#             or load('company_id', self.env['res.company']).currency_id
#             or self.env['res.currency']
#         )

#         return {
#             **kwargs,
#             'record': record,
#             'id': load('id', 0),

#             # Basic fields:
#             'product_id': load('product_id', self.env['product.product']),
#             'tax_ids': load('tax_ids', self.env['account.tax']),
#             'price_unit': load('price_unit', 0.0),
#             'professional_fees': load('professional_fees', 0.0),
#             'quantity': load('quantity', 0.0),
#             'discount': load('discount', 0.0),
#             'currency_id': currency,

#             # The special_mode for the taxes computation:
#             # - False for the normal behavior.
#             # - total_included to force all taxes to be price included.
#             # - total_excluded to force all taxes to be price excluded.
#             'special_mode': kwargs.get('special_mode', False),

#             # A special typing of base line for some custom behavior:
#             # - False for the normal behavior.
#             # - early_payment if the base line represent an early payment in mixed mode.
#             # - cash_rounding if the base line is a delta to round the business object for the cash rounding feature.
#             'special_type': kwargs.get('special_type', False),

#             # All computation are managing the foreign currency and the local one.
#             # This is the rate to be applied when generating the tax details (see '_add_tax_details_in_base_line').
#             'rate': load('rate', 1.0),

#             # For all computation that are inferring a base amount in order to reach a total you know in advance, you have to force some
#             # base/tax amounts for the computation (E.g. down payment, combo products, global discounts etc).
#             'manual_tax_amounts': kwargs.get('manual_tax_amounts', None),

#             # ===== Accounting stuff =====

#             # The sign of the business object regarding its accounting balance.
#             'sign': load('sign', 1.0),

#             # If the document is a refund or not to know which repartition lines must be used.
#             'is_refund': load('is_refund', False),

#             # If the tags must be inverted or not.
#             'tax_tag_invert': load('tax_tag_invert', False),

#             # Extra fields for tax lines generation:
#             'partner_id': load('partner_id', self.env['res.partner']),
#             'account_id': load('account_id', self.env['account.account']),
#             'analytic_distribution': load('analytic_distribution', None),
#             'deferred_start_date': load('deferred_start_date', False),
#             'deferred_end_date': load('deferred_end_date', False),
#         }

#     def _prepare_product_base_line_for_taxes_computation(self, product_line):
#         """ Convert an account.move.line having display_type='product' into a base line for the taxes computation.

#         :param product_line: An account.move.line.
#         :return: A base line returned by '_prepare_base_line_for_taxes_computation'.
#         """
#         self.ensure_one()
#         is_invoice = self.is_invoice(include_receipts=True)
#         sign = self.direction_sign if is_invoice else 1
#         if is_invoice:
#             rate = self.invoice_currency_rate
#         else:
#             rate = (abs(product_line.amount_currency) / abs(product_line.balance)) if product_line.balance else 0.0

#         return self.env['account.tax']._prepare_base_line_for_taxes_computation(
#             product_line,
#             price_unit=product_line.price_unit if is_invoice else product_line.amount_currency,
#             professional_fees=product_line.professional_fees if is_invoice else product_line.amount_currency,
#             quantity=product_line.quantity if is_invoice else 1.0,
#             discount=product_line.discount if is_invoice else 0.0,
#             rate=rate,
#             sign=sign,
#             special_mode=False if is_invoice else 'total_excluded',
#         )