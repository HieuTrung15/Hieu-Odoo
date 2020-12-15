from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VoucherRule(models.Model):
    _name = 'voucher.rule'
    _description = 'Voucher Rule'

    amount_from = fields.Float(string="Amount from", required=True)
    amount_to = fields.Float(string="Amount to", required=True)
    discount_percentage = fields.Float(string="Discount", default=0,
                                       help='The discount in percentage, between 1 to 100')
    voucher_program_id = fields.Many2one('voucher.program', ondelete='cascade')

    @api.constrains('discount_percentage')
    def _check_discount_percentage(self):
        for res in self:
            if not 0 < res.discount_percentage <= 100:
                raise ValidationError('The discount in percentage must be between 1 to 100')

    @api.constrains('amount_from')
    def _check_amount_from_rule(self):
        for res in self:
            if res.amount_from < 0:
                raise ValidationError('The amount to apply a discount voucher should be greater than 0')

    @api.constrains('amount_to')
    def _check_amount_to_rule(self):
        for res in self:
            if res.amount_to < 0 or res.amount_to < res.amount_from:
                raise ValidationError('The amount should be greater than 0 and the beginning amount')
