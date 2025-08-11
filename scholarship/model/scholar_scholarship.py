from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError, ValidationError
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


def get_scholarship_states(env):
    stages = env['scholarship.stages'].search([], order='sequence asc')
    if not stages:
        default_stages = ['New', 'Approved', 'Rejected']
        for idx, name in enumerate(default_stages, start=1):
            env['scholarship.stages'].sudo().create({
                'sequence': idx,
                'stage': name,
            })
        stages = env['scholarship.stages'].search([], order='sequence asc')
    return [(stage.stage.lower(), stage.stage) for stage in stages]

class Scholarship(models.Model):
    _name = 'scholarship.scholarship'
    _description = 'Scholarship Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  

    name = fields.Char(readonly=True, copy=False, default='/', tracking=True)
    form_no = fields.Char(string="Form no.")

    state = fields.Selection(
        selection=lambda self: get_scholarship_states(self.env),
        string='Status',
        default=lambda self: get_scholarship_states(self.env)[0][0],
        tracking=True
    )

    student_id = fields.Many2one('res.partner', string="Student",domain=[('supplier_rank','>',0)], required=True)
    grn_cid = fields.Char(string="GRN / CID")

    campus_id = fields.Many2one('scholarship.campus', string="Campus",ondelete='set null')
    class_id = fields.Many2one('scholarship.class', string="Class", ondelete='set null')
    section_id = fields.Many2one('scholarship.section', string="Section", ondelete='set null')
    category_id = fields.Many2one('scholarship.category', string="Category", ondelete='set null')
    staff_category_id = fields.Many2one('scholarship.staff.category', string="Staff Category", ondelete='set null')

    date_from = fields.Datetime("Start Date", required=True)
    date_to = fields.Datetime("End Date", required=True)

    donor_group= fields.Many2one('donor.group',string="Donor category")
    donor_sub_category= fields.Many2one('donor.sub.group', string="Donor sub category")
    donor_id = fields.Many2one('res.partner', string="Donor", required=True)
    result = fields.Float(string="Result (%)")
    monthly_fee = fields.Monetary(string="Monthly Fee")
    discount = fields.Selection(selection=[
        ('100','100'),
        ('50','50'),
        ('25','25'),
    ],string="Discount (%)")

    annual_discount = fields.Monetary(string="Annual Discount", compute="_compute_annual_discount", store=True)

    @api.depends('monthly_fee', 'discount')
    def _compute_annual_discount(self):
        for rec in self:
            if rec.monthly_fee and rec.discount:
                rec.annual_discount = ( (rec.monthly_fee * float(rec.discount))/100 ) * 12
            else:
                rec.annual_discount = 0.0

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    tag_ids = fields.Many2many('scholarship.tags', string="Tags")
    line_ids = fields.One2many('scholarship.line', 'scholarship_id', string='Details',ondelete='cascade')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('scholarship.scholarship') or '/'
            _logger.info("Creating Scholarship with name: %s", vals['name'])
        return super(Scholarship, self).create(vals)

    def calculate_total_months(self):
        start = fields.Datetime.from_string(self.date_from)
        end = fields.Datetime.from_string(self.date_to)

        diff = relativedelta(end, start)
        total_months = diff.years * 12 + diff.months + 1  
        self.state = 'new' 
        return total_months
    
    def approve_scholarship(self):
        self.ensure_one()

        journal = self.env['account.journal'].search([('name', '=', 'Scholarship')], limit=1)
        if not journal:
            journal = self.env['account.journal'].create({
                'name': 'Scholarship',
                'type': 'general',
                'code': 'SCH',
                'company_id': self.env.company.id,
            })

        self.line_ids.write({'status': 'approved'})

        donor = self.donor_id
        student= self.student_id
        if not donor.property_account_receivable_id :
            raise UserError(_("Donor must have Receivable accounts configured."))

        if not student.property_account_payable_id:
            raise UserError(_("Donor must have Receivable accounts configured."))
            
        receivable_account = donor.property_account_receivable_id.id
        payable_account = student.property_account_payable_id.id

        for line in self.line_ids:
            amount = line.fee
            if amount <= 0.0:
                continue
            
            if line.status == 'approved':
                move_vals = {
                    'journal_id': journal.id,
                    'date': line.date,
                    'ref': f"{self.name}-{line.id}",
                    'line_ids': [
                        (0, 0, {
                            'account_id': receivable_account,
                            'partner_id': donor.id,
                            'name': 'Scholarship Receivable',
                            'debit': 0.0,
                            'credit': amount,
                        }),
                        (0, 0, {
                            'account_id': payable_account,
                            'partner_id': student.id,
                            'name': 'Scholarship Payable',
                            'debit': amount,
                            'credit': 0.0,
                        }),
                    ]
                }

                move = self.env['account.move'].create(move_vals)
            
        self.state = 'approved'

        return {
            'type': 'ir.actions.client',
            'tag': 'custom.notification_reload',
            'params': {
                'title': _('Success 🎉'),
                'message': _('Journal Entries created and Scholarship approved successfully!'),
                'sticky': False,
                'type': 'success',
                'delay':500,
            }
        }

    def reject_scholarship(self):
        self.ensure_one()
        journal_entries = self.env['account.move'].search([
            ('ref', '=', self.name),
            ('state', '=', 'draft')
        ])
        if journal_entries:
            for move in journal_entries:
                move.button_cancel()

        self.line_ids.write({'status': 'rejected'})

        self.state = 'rejected'
        return {
            'type': 'ir.actions.client',
            'tag': 'custom.notification_reload',
            'params': {
                'title': _('Rejected 🔕'),
                'message': _('Scholarship rejected!'),
                'sticky': False,
                'type': 'danger',
                'delay':500,
            }
        }
    def reset_scholarship(self):
        self.ensure_one()
        self.state ='draft'
        self.line_ids.unlink()
        
    def action_calculate_lines(self):
        self.ensure_one()
        self.line_ids.unlink()

        start = fields.Datetime.from_string(self.date_from)
        end = fields.Datetime.from_string(self.date_to)
        date = start

        total_months = self.calculate_total_months()
        monthly_amount = self.annual_discount / total_months if total_months else 0.0
        donor_balance = self.donor_id.credit - self.donor_id.debit

        used_balance = 0.0
        created_lines = 0

        while date <= end:
            if used_balance + monthly_amount <= donor_balance:
                self.env['scholarship.line'].create({
                    'scholarship_id': self.id,
                    'date': date.date(),
                    'funds': self.donor_id.name,
                    'description': 'Fund',
                    'fee': monthly_amount,
                    'status': 'approved',
                })
                used_balance += monthly_amount
                created_lines += 1
                date += relativedelta(months=1)
            else:
                break

        if created_lines == 0:
            raise UserError(_(
                f"{self.donor_id.name} doesn't have enough funds to cover even one month of scholarship 😞"
            ))

        if created_lines < total_months:
            return {
                'type': 'ir.actions.client',
                'tag': 'custom.notification_reload',
                'params': {
                    'title': _('Partial Funding ⚠️'),
                    'message': _(
                        f"{self.donor_id.name} doesn't have enough funds to cover the full scholarship period.\n"
                        f"Only {created_lines} out of {total_months} month(s) funded. 😞"
                    ),
                    'type': 'warning',
                    'delay': 500
                }
            }


        return {
            'type': 'ir.actions.client',
            'tag': 'custom.notification_reload',
            'params': {
                'title': _('Lines Created 🎉'),
                'message': _('All scholarship lines created successfully!'),
                'sticky': False,
                'type': 'success',
                'delay': 500
            }
        }


    @api.onchange('grn_cid')
    def _onchange_grn_cid(self):
        for rec in self:
            student=rec.env['res.partner'].search([('grn_no','=',rec.grn_cid)], limit=1)
        
            rec.student_id= student.id or False
            rec.campus_id = student.campus_id.id if student.campus_id else False
            rec.class_id = student.class_id.id if student.class_id else False
            rec.section_id = student.section_id.id if student.section_id else False


    @api.onchange('discount', 'category_id')
    def _check_discount_category_constraint(self):
        for rec in self:
            if not rec.discount:
                return;

            if rec.category_id.name == 'STAFF SCHOLARSHIP' or rec.category_id.name == 'NEED-BASED SCHOLARSHIP':
                if rec.discount not in ['100', '50']:
                    rec.discount = False
                    return {
                        'warning': {
                            'title': 'Invalid Discount',
                            'message': 'Only 100% or 50% discounts are allowed for this category.',
                        }
                    }
            elif rec.category_id.name == 'SIBLING DISCOUNT':
                if rec.discount not in ['25']:
                    rec.discount = False
                    return {
                        'warning': {
                            'title': 'Invalid Discount',
                            'message': 'Only 25% discount is allowed for this category.',
                        }
                    }
            else:
                break;

    def bulk_computes_scholarship_lines(self):
        for rec in self:
            _logger.info("Processing Scholarship ID: %s", rec.id)
            if rec.state != 'draft':
                raise UserError(_("Scholarship must be in draft state to compute lines."))
            rec.action_calculate_lines()
            rec.state = 'new'
    def bulk_approve_scholarship(self):
        for rec in self:
            _logger.info("Processing Scholarship ID: %s", rec.id)
            if rec.state != 'new':
                raise UserError(_("Scholarship must be in new state to approve lines."))
            rec.approve_scholarship()
            rec.state = 'approved'

    def bulk_reject_scholarship(self):
        for rec in self:
            _logger.info("Processing Scholarship ID: %s", rec.id)
            if rec.state in ['new', 'partial rejected']:
                raise UserError(_("Scholarship must be in new or partial rejected state to reject lines."))
            rec.reject_scholarship()
            rec.state = 'rejected'

    def reject_scholarship_lines(self):
        for rec in self:
            lines = rec.line_ids.sorted(key=lambda x: x.id)
            found_rejected = False
            selected_remarks = ""
            for line in lines:
                if found_rejected or line.status == 'rejected':
                    if not found_rejected:
                        found_rejected = True
                        selected_remarks = line.remarks

                    line.write({
                        'status': 'rejected',
                        'remarks': selected_remarks
                    })
                    rec.write({'state': 'partial rejected'})
                    
            rejected_lines = rec.line_ids.filtered(lambda l: l.status == 'rejected')
            
            for line in rejected_lines:
                journal_entries = rec.env['account.move'].search([
                    ('ref', '=', f"{rec.name}-{line.id}"),
                    ('state', '=', 'draft'),
                ])
                for move in journal_entries:
                    move.button_cancel()