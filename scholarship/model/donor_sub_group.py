from odoo import models, fields, api,_

class Donor_sub_group(models.Model):
    _name="donor.sub.group"
    _description="Donor Sub Group"
    _order="sequence"
    
    name=fields.Char(string="Sub Category")
    sequence=fields.Integer(string="Sequence")