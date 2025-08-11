from odoo import models, fields

class ScholarshipCategory(models.Model):
    _name = 'scholarship.category'
    _description = 'Scholarship Category'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
