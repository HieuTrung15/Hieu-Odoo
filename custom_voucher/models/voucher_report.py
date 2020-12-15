from odoo import models, fields


class VoucherReport(models.Model):
    _name = "voucher.report"
    _description = "Voucher report"

    partner_id = fields.Many2one('res.partner')
    order_ids = fields.One2many('sale.order', 'voucher_report_id', 'Orders')
    sales_achieved = fields.Float('Sales Achieved')
    reward = fields.Float('Reward')
    voucher_program_id = fields.Many2one('voucher.program')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    voucher_report_id = fields.Many2one('voucher.report')
