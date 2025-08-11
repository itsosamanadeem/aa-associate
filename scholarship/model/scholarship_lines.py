from odoo import models, fields,api,_

def get_scholarship_remarks(env):
    default_remarks = [
        "Incomplete Documentation",
        "Does Not Meet Eligibility Criteria",
        "Insufficient Academic Performance",
        "Exceeded Scholarship Quota",
        "Funding Not Available",
        "Late Application Submission",
        "Missing Fee Payment",
        "Disciplinary Issues",
        "Previously Awarded Scholarship",
        "Failed Verification Process"
    ]
    
    remarks = env['scholarship.lines.remarks'].search([], order='sequence asc')
    if not remarks:
        for idx, name in enumerate(default_remarks, start=1):
            env['scholarship.lines.remarks'].sudo().create({
                'sequence': idx,
                'remark': name,
            })
        remarks = env['scholarship.lines.remarks'].search([], order='sequence asc')
    
    return [(remark.remark.lower().replace(" ", "_"), remark.remark) for remark in remarks]

class ScholarshipLine(models.Model):
    _name = 'scholarship.line'
    _description = 'Scholarship Line'
    _rec_name="scholarship_id"
    
    scholarship_id = fields.Many2one('scholarship.scholarship', string='Scholarship')
    student_name = fields.Char(related="scholarship_id.student_id.name", store=True, string="Student")
    donor_name = fields.Char(related="scholarship_id.donor_id.name", store=True, string="Donor")
    date = fields.Date()
    funds = fields.Char(compute="_compute_fund_raiser", store=True)
    @api.depends('scholarship_id.donor_id')
    def _compute_fund_raiser(self):
        for rec in self:
            rec.funds= rec.scholarship_id.donor_id.name

    description = fields.Char()
    fee = fields.Float()
    status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='approved')
    remarks = fields.Selection(
        selection=lambda self: get_scholarship_remarks(self.env),
        string="Remarks",
        default=lambda self: get_scholarship_remarks(self.env)[0][0],
        tracking=True
    )

    
