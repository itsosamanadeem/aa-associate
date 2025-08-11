from odoo import models, fields

class ScholarshipSection(models.Model):
    _name = 'scholarship.section'
    _description = 'Scholarship Section'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
