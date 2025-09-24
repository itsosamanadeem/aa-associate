# models/account_move.py
from odoo import models, api

class AccountMove(models.Model):
    _inherit = "account.move"

    def get_taxes_values(self):
        """
        Override tax base calculation so taxes are computed on the line's
        professional_fees (per-unit) instead of the usual price_unit.
        """
        tax_grouped = {}
        # follow Odoo pattern: iterate invoices (the original also does this)
        for inv in self:
            tax_grouped = {}
            for line in inv.invoice_line_ids:
                # Use professional_fees as the taxable price_unit if present,
                # otherwise fall back to the normal price_unit.
                price_unit_for_tax = line.professional_fees if line.professional_fees else line.price_unit
                # apply discount like Odoo usually does (if you don't want discount to apply to professional_fees remove the next line)
                price_unit_for_tax = price_unit_for_tax * (1 - (line.discount or 0.0) / 100.0)

                # compute taxes (same signature as Odoo's compute_all)
                taxes = line.tax_ids.compute_all(
                    price_unit_for_tax,
                    currency=inv.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=inv.partner_id,
                ).get('taxes', [])

                for tax in taxes:
                    val = self._prepare_tax_line_vals(line, tax)
                    key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)
                    if key not in tax_grouped:
                        tax_grouped[key] = val
                    else:
                        tax_grouped[key]['amount'] += val['amount']
                        tax_grouped[key]['base'] += val['base']
        return tax_grouped
