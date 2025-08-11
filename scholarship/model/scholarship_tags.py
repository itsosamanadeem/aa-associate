from odoo import models, fields

class ScholarshipTag(models.Model):
    _name = 'scholarship.tags'
    _description = 'Scholarship Tag'
    _order = 'sequence'
    _rec_name = "tag"

    tag = fields.Char(required=True)
    sequence = fields.Integer(default=10)
