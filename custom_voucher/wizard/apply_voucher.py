from odoo import fields, models
from odoo.exceptions import ValidationError


class ApplyVoucher(models.TransientModel):
    _name = 'apply.voucher'
    _description = 'Apply Voucher on Sale Order'

    voucher_code = fields.Char(string="Code", required=True)
    order_id = fields.Many2one('sale.order', readonly=True)

    def apply_voucher(self):
        current_order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        voucher_num = self.env['voucher'].sudo().search([('code', '=', self.voucher_code)], limit=1)
        voucher_product_id = self.env.ref('custom_voucher.voucher_code').id
        voucher_pro = self.env['voucher.program'].search([('id', '=', voucher_num.voucher_program_id.id)])
        if not voucher_num:
            raise ValidationError('The code is invalid!')
        if voucher_num._check_voucher_code(current_order):
            raise ValidationError('The code has been used or expired')
        if not voucher_num.partner_id == current_order.partner_id:
            raise ValidationError("You don't have the permission to use this Code!")
        if current_order.amount_untaxed <= 0:
            raise ValidationError('Pick products first!')
        order = voucher_num.sale_order_id
        if order:
            if order.state == 'draft':
                for item in order.order_line:
                    if item.product_id.id == voucher_pro.discount_product_id.id:
                        item.unlink()
            elif order.state == 'sale':
                voucher_num.write({'state': 'used'})
        value = {
            'product_id': voucher_product_id,
            'name': ('Discount for customer: %s') % current_order.partner_id.name,
            'qty_delivered': 1,
            'price_unit': - self._check_reward(voucher_num.reward),
            'tax_id': False,
        }
        if voucher_product_id in current_order.order_line.mapped('product_id').ids:
            raise ValidationError('This voucher has been applied to the current order.')
        else:
            current_order.write({'order_line': [(0, False, value)]})
            voucher_num.write({'sale_order_id': current_order.id})

    def _check_reward(self, reward):
        voucher_num = self.env['voucher'].sudo().search([('code', '=', self.voucher_code)], limit=1)
        current_order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        if voucher_num.reward > current_order.amount_untaxed:
            reward = sum(price.price_subtotal for price in current_order.order_line)
        else:
            reward = voucher_num.reward
        return reward
