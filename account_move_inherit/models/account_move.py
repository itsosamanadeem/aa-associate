# models/account_move.py
from odoo import models, api, _, fields
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    def _prepare_product_base_line_for_taxes_computation(self, product_line):
        """ Convert an account.move.line having display_type='product' into a base line for the taxes computation.

        :param product_line: An account.move.line.
        :return: A base line returned by '_prepare_base_line_for_taxes_computation'.
        """
        self.ensure_one()
        is_invoice = self.is_invoice(include_receipts=True)
        sign = self.direction_sign if is_invoice else 1
        if is_invoice:
            rate = self.invoice_currency_rate
        else:
            rate = (abs(product_line.amount_currency) / abs(product_line.balance)) if product_line.balance else 0.0

        return self.env['account.tax']._prepare_base_line_for_taxes_computation(
            product_line,
            price_unit=product_line.professional_fees if is_invoice else product_line.amount_currency,
            quantity=product_line.quantity if is_invoice else 1.0,
            discount=product_line.discount if is_invoice else 0.0,
            rate=rate,
            sign=sign,
            special_mode=False if is_invoice else 'total_excluded',
        )
    # @api.depends(
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.origin_payment_id.is_matched',
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.origin_payment_id.is_matched',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
    #     'line_ids.balance',
    #     'line_ids.currency_id',
    #     'line_ids.amount_currency',
    #     'line_ids.amount_residual',
    #     'line_ids.amount_residual_currency',
    #     'line_ids.payment_id.state',
    #     'line_ids.full_reconcile_id',
    #     'line_ids.professional_fees',
    #     'state')
    # def _compute_amount(self):
    #     for move in self:
    #         total_untaxed, total_untaxed_currency = 0.0, 0.0
    #         total_tax, total_tax_currency = 0.0, 0.0
    #         total_residual, total_residual_currency = 0.0, 0.0
    #         total, total_currency = 0.0, 0.0

    #         for line in move.line_ids:
    #             if move.is_invoice(True):
    #                 # === Invoices ===
    #                 if line.display_type == 'tax' or (line.display_type == 'rounding' and line.tax_repartition_line_id):
    #                     # Tax amount.
    #                     total_tax += line.professional_fees
    #                     total_tax_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                     # raise UserError('1')
    #                 elif line.display_type in ('product', 'rounding'):
    #                     # Untaxed amount.
    #                     total_untaxed += line.professional_fees
    #                     total_untaxed_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                     # raise UserError(f"{line.name} - Total: {total}, Total Currency: {total_currency}, Tax: {total_untaxed}, Tax Currency: {total_untaxed_currency}")
    #                     # raise UserError('2')
    #                 elif line.display_type == 'payment_term':
    #                     # Residual amount.
    #                     total_residual += line.amount_residual
    #                     total_residual_currency += line.amount_residual_currency
    #                     # raise UserError('3')
    #             else:
    #                 # === Miscellaneous journal entry ===
    #                 if line.debit:
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                     # raise UserError('4')

    #             # raise UserError(_("Line: %s, Balance: %s, Amount Currency: %s") % (line.name, line.balance, line.amount_currency))

    #         sign = move.direction_sign
    #         # raise UserError(sign)
    #         move.amount_untaxed = sign * total_untaxed_currency
    #         move.amount_tax = sign * total_tax_currency
    #         move.amount_total = sign * total_currency
    #         move.amount_residual = -sign * total_residual_currency
    #         move.amount_untaxed_signed = -total_untaxed
    #         move.amount_untaxed_in_currency_signed = -total_untaxed_currency
    #         move.amount_tax_signed = -total_tax
    #         move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
    #         move.amount_residual_signed = total_residual
    #         move.amount_total_in_currency_signed = abs(move.amount_total) if move.move_type == 'entry' else -(sign * move.amount_total)

    #         # raise UserError(_("Total Untaxed: %s, Total Tax: %s, Total: %s, Total Residual: %s") % (total_untaxed, move.amount_tax_signed, total, total_residual))
    
    # @api.depends_context('lang')
    # @api.depends(
    #     'invoice_line_ids.currency_rate',
    #     'invoice_line_ids.tax_base_amount',
    #     'invoice_line_ids.tax_line_id',
    #     'invoice_line_ids.price_total',
    #     'invoice_line_ids.price_subtotal',
    #     'invoice_payment_term_id',
    #     'partner_id',
    #     'currency_id',
    # )
    # def _compute_tax_totals(self):
    #     """ Computed field used for custom widget's rendering.
    #         Only set on invoices.
    #     """
    #     for move in self:
    #         if move.is_invoice(include_receipts=True):
    #             base_lines, _tax_lines = move._get_rounded_base_and_tax_lines()
    #             raise UserError(f"Tax Totals: {base_lines}, {_tax_lines}")
    #             move.tax_totals = self.env['account.tax']._get_tax_totals_summary(
    #                 base_lines=base_lines,
    #                 currency=move.currency_id,
    #                 company=move.company_id,
    #                 cash_rounding=move.invoice_cash_rounding_id,
    #             )
    #             move.tax_totals['display_in_company_currency'] = (
    #                 move.company_id.display_invoice_tax_company_currency
    #                 and move.company_currency_id != move.currency_id
    #                 and move.tax_totals['has_tax_groups']
    #                 and move.is_sale_document(include_receipts=True)
    #             )
    #         else:
    #             # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
    #             move.tax_totals = None