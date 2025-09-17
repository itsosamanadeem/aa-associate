# models/account_reconcile_wizard.py
from odoo import fields, models

class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.reconcile.wizard"

    check_date = fields.Date(string="Check Date")
    check_number = fields.Char(string="Check Number")
