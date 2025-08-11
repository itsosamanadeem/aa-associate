from odoo import models, fields
class ResPartner(models.Model): 
    _inherit = "res.partner"

    donor_group= fields.Many2one('donor.group', string="Donor Category", ondelete='set null')