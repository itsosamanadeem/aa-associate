from odoo import fields, models

class AccountReconcileWizard(models.TransientModel):
    _inherit = "account.payment.register"

    check_date = fields.Date(string="Check Date")
    check_number = fields.Char(string="Check Number")

    def _create_payment_vals_from_wizard(self, batch_result):
        """Extend to add check fields into created payments"""
        vals_list = super()._create_payment_vals_from_wizard(batch_result)
        vals_list.update({
            "check_date": self.check_date,
            "check_number": self.check_number,
        })
        return vals_list


class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_date = fields.Date(string="Check Date", readonly=True,)
    check_number = fields.Char(string="Check Number",readonly=True,)
