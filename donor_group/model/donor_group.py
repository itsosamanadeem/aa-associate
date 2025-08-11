from odoo import models, fields

class DonorGroup(models.Model):
    _name = "donor.group"
    _description = "Donor Category"
    _rec_name = "description"
    _order="sequence"

    description = fields.Many2one('res.partner',  domain=[('customer_rank','>',0)],required=True)
    contact = fields.Char(string="Contact Person")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    sequence = fields.Integer(default=10)
