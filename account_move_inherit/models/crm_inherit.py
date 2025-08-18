from odoo import models, fields

class ResPartnerTrademark(models.Model):
    _name = "res.partner.trademark"
    _description = "Partner Trademark"
    _order = "sequence, id"
    _rec_name = "trademark_name"
    
    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one("res.partner", string="Partner", ondelete="cascade")
    trademark_name = fields.Char(string="Trademark Name")
    trademark_number = fields.Char(string="Trademark Number")
    name = fields.Char(string="Display Name")  # can hold formatted label

class ResPartner(models.Model):
    _inherit = "res.partner"

    associated_trademark_ids = fields.One2many(
        "res.partner.trademark", "partner_id", string="Associated Trademarks"
    )

class CrmLead(models.Model):
    _inherit = "crm.lead"

    associated_trademark_ids = fields.One2many(
        related="partner_id.associated_trademark_ids",
        string="Associated Trademarks",
        readonly=False
    )
