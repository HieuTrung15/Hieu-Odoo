from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    applied_voucher_ids = fields.One2many('voucher', 'sale_order_id', string="Applied Vouchers")
    is_customer = fields.Boolean(compute='_customer_checking')

    @api.depends('partner_id')
    def _customer_checking(self):
        for res in self:
            customer_id = self.env['voucher'].search([]).filtered(lambda r: r.partner_id == self.partner_id)
            res.is_customer = any(customer for customer in customer_id)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.applied_voucher_ids.write({'state': 'used'})
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        self.applied_voucher_ids.write({'state': 'new'})
        return res

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        product_ids = self.order_line.mapped('product_id')
        voucher_product_id = self.env.ref('custom_voucher.voucher_code').id
        for rec in self:
            if voucher_product_id not in product_ids.ids:
                rec.env['voucher'].search([('sale_order_id', '=', rec.id)]).write({'sale_order_id': None})
            return res
