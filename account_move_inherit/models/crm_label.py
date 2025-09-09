from odoo import models, fields, api, _

class ResPartnerTrademark(models.Model):
    _name = "res.partner.label"
    _description = "Partner Trademark"
    _order = "sequence, id"
    _rec_name = "label"
    
    sequence = fields.Integer(default=10)
    label= fields.Char(string="Label", required=True)
