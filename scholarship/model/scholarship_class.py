from odoo import models, fields

class ScholarshipClass(models.Model):
    _name = 'scholarship.class'
    _description = 'Scholarship Class'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

