from odoo import models, fields,_,api

class Scholarship_Stages(models.Model):
    _name="scholarship.stages"
    _description="Scholarship Stages"
    _order= "sequence"
    
    sequence= fields.Integer(string="Sequence",default=10)
    stage = fields.Char(string="Stage", requried=True)