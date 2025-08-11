from odoo import models, fields

class ScholarshipCampus(models.Model):
    _name = 'scholarship.campus'
    _description = 'Scholarship Campus'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

