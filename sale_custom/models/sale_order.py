from odoo import fields, models, api


class SaleCustom(models.Model):
    _inherit = ['sale.order']

    un_disc = fields.Monetary(string="UnDiscount", compute='_compute_discount')
    disc = fields.Monetary(string="Discount", compute='_compute_discount')


    @api.depends('order_line')
    def _compute_discount(self):
        order_line = self.order_line
        un_disc = 0.0
        disc = 0.0
        for item in order_line:
            price = item.price_unit
            un_disc += price
            disc += price * item.discount / 100
        self.un_disc = un_disc
        self.disc = disc

    @api.onchange('partner_id', 'order_line')
    def _onchange_check(self):
        partner_id = self.partner_id.id
        if not self.partner_id or not self.order_line:
            return False

        order_partner_id = self.env['res.users'].sudo().search([('partner_id', '=', partner_id)])

        if not order_partner_id:
            return False

        self.order_line.write({'discount': 20})
    #
    # @api.onchange('order_line')
    # def _change_tax(self):
    #     # product_list = []
    #     product_list = self.env['product.template'].sudo().search(['type', '=', 'service'])
    #     if self.order_line.product_id.name in product_list:
    #         self.order_line.write({'tax_id': 20})





