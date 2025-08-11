from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    grn_no = fields.Char(string="GR No.")
    campus_id = fields.Many2one('scholarship.campus', string="Campus", ondelete='set null')
    class_id = fields.Many2one('scholarship.class', string="Class", ondelete='set null')
    section_id = fields.Many2one('scholarship.section', string="Section", ondelete='set null')

    def open_scholarship_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scholarships',
            'res_model': 'scholarship.scholarship',
            'view_mode': 'list,form',
            # 'domain': [('student_id', '=', self.id)],
            # 'context': {'default_student_id': self.id},
        }
