from odoo import models, fields

class ScholarLinesRemarks(models.Model):
    _name = 'scholarship.lines.remarks'
    _description = 'Scholarship Lines Remarks'
    _order = 'sequence'

    sequence = fields.Integer(default=10)
    remark = fields.Char(required=True)
