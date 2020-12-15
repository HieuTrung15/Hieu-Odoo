from dateutil.relativedelta import relativedelta
from odoo import models, fields
from odoo.exceptions import ValidationError


class Voucher(models.Model):
    _name = "voucher"
    _description = "Voucher"
    _rec_name = "code"

    code = fields.Char(required=True, readonly=True)
    reward = fields.Float('Reward', readonly=True)
    expiration_date = fields.Date('Expiration Date', compute='_compute_expiration_date', readonly=True)
    partner_id = fields.Many2one('res.partner', "For Customer", readonly=True)
    voucher_program_id = fields.Many2one('voucher.program', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Applied on order', readonly=True)

    state = fields.Selection([
        ('new', 'Valid'),
        ('used', 'Consumed'),
        ('expired', 'Expired')
    ], require=False, default='new')

    def _compute_expiration_date(self):
        self.expiration_date = 0
        for voucher in self.filtered(lambda x: x.voucher_program_id.validity_duration > 0):
            voucher.expiration_date = (
                    voucher.create_date + relativedelta(days=voucher.voucher_program_id.validity_duration)).date()

    def _check_voucher_code(self, order):
        for rec in self:
            if rec.state in ('used', 'expired') or \
                    (rec.expiration_date and rec.expiration_date < order.date_order.date()):
                raise ValidationError('This voucher %s has been used or is expired')
