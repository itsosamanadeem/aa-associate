from odoo import api, fields, models


class AccountMoveSendWizard(models.TransientModel):
    _inherit = "account.move.send.wizard"

    mail_cc = fields.Char(
        string="CC",
        help="Comma-separated CC email addresses",
        readonly=False,
        store=True,
    )

    @api.depends('mail_template_id', 'mail_lang')
    def _compute_mail_subject_body_partners(self):
        """Extend default compute to also fetch email_to and email_cc from template"""
        super()._compute_mail_subject_body_partners()
        for wizard in self:
            if wizard.mail_template_id:
                # Parse template's email_to and email_cc
                email_to = wizard.mail_template_id.email_to
                email_cc = wizard.mail_template_id.email_cc

                # Convert email_to (string) into partners if possible
                if email_to:
                    partners = self.env['res.partner'].search([('email', 'in', [e.strip() for e in email_to.split(',')])])
                    wizard.mail_partner_ids = [(6, 0, partners.ids)]

                # Store email_cc directly
                if email_cc:
                    wizard.mail_cc = email_cc
