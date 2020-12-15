from odoo import fields, models, api


class SaleCommission(models.Model):
    _name = 'sale.commission'

    name = fields.Char(string="Name of commission", required=True)
    type_of_commission = fields.Selection([
        ('permanent', 'Permanent'),
        ('section', 'Section')
    ], default='section')
    base_money = fields.Selection([
        ('total_money','Total Money'),
        ('net_money','Net Money')
    ], default='net_money')
    status_invoice = fields.Selection([
        ('invoice_based', 'Invoice Based'),
        ('payment_based', 'Payment Based')
    ], default='invoice_based')
    percent_permanent = fields.Integer(string="Percent Permanent")

    section_money_ids = fields.One2many('section.money', 'sale_commission_id', string="Section List")











