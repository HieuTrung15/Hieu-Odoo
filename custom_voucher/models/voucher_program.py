import random
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VoucherProgram(models.Model):
    _name = "voucher.program"
    _description = "Voucher Program"

    name = fields.Char(string="Name", required=True)
    date_from = fields.Datetime(string="Start Date", help="Voucher program start date")
    date_to = fields.Datetime(string="End Date", help="Voucher program end date")
    partner_tag_ids = fields.Many2many('res.partner.category', string="Ca")
    voucher_rule_ids = fields.One2many('voucher.rule', 'voucher_program_id', string="Rule")
    voucher_report_ids = fields.One2many('voucher.report', 'voucher_program_id', string="Report")
    voucher_ids = fields.One2many('voucher', 'voucher_program_id', string="Voucher")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('expired', 'Expired')
    ], required=True, default='draft')
    validity_duration = fields.Integer(help="Validity duration for a coupon after its generation")
    discount_product_id = fields.Many2one('product.product', readonly=False, ondelete='cascade')

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'draft'

    @api.constrains('date_from', 'date_to')
    def _check_date_from(self):
        if any(rec for rec in self
               if rec.date_to and rec.date_from and rec.date_to < rec.date_from):
            raise ValidationError('The start date must be before the end date')

    def action_view_report(self):
        voucher_report = self.env['voucher.report'].sudo()
        voucher_report.search([('voucher_program_id', '=', self.id)]).unlink()
        sale_order = self.env['sale.order'].sudo()
        partner_ids = self.partner_tag_ids.partner_ids.mapped('id')
        date_from = self.date_from
        date_to = self.date_to
        voucher_program_id = self.id
        voucher_rule = self.env['voucher.rule'].sudo()
        vals = ()
        for partner_id in partner_ids:
            domain = [('partner_id', '=', partner_id), ('date_order', '>=', date_from),
                      ('date_order', '<', date_to)]
            partner_orders = sale_order.search(domain)
            amount_total = 0
            for order in partner_orders:
                amount_total += order.amount_untaxed
            domain = [('voucher_program_id', '=', self.id), ('amount_from', '<', amount_total),
                      ('amount_to', '>=', amount_total)]
            voucher_rule_id = voucher_rule.search(domain)
            reward = voucher_rule_id.discount_percentage * amount_total / 100
            vals += ({
                         'partner_id': partner_id,
                         'order_ids': partner_orders.ids,
                         'sales_achieved': amount_total,
                         'voucher_program_id': voucher_program_id,
                         'reward': reward,
                     },)
        if not vals:
            return False
        return voucher_report.create(vals)

    def action_create_voucher(self):
        voucher = self.env['voucher'].sudo()
        voucher.search([('voucher_program_id', '=', self.id)]).unlink()
        voucher_report_ids = self.voucher_report_ids
        vals = ()
        voucher_program_id = self.id
        expiration_date = self.env['voucher'].expiration_date
        for voucher_report in voucher_report_ids:
            vals += ({
                         'partner_id': voucher_report.partner_id.id,
                         'code': str(random.getrandbits(64)),
                         'reward': voucher_report.reward,
                         'voucher_program_id': voucher_program_id,
                         'expiration_date': expiration_date,
                     },)
        if not vals:
            return False
        return voucher.create(vals)
