from odoo import fields, models, api


class SectionMoney(models.Model):
    _name = 'section.money'

    from_money = fields.Integer(string="From Money")
    to_money = fields.Integer(string="To Money")
    percentage = fields.Integer(string="Percentage")
    sale_commission_id = fields.Many2one('sale.commission', string="Section ID")
