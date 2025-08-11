from odoo import models, fields

class ScholarshipStaffCategory(models.Model):
    _name = 'scholarship.staff.category'
    _description = 'Scholarship Staff Category'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
