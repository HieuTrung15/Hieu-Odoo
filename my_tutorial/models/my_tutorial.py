from odoo import models, fields


class MyTutorial(models.Model):
    _name = 'my.tutorial'

    name = fields.Char(string="Name", required=True)
    short_name = fields.Char(string="Short Name")
    contact_name = fields.Char(string="Contact Name")
    address = fields.Char(string="Address")
    desc = fields.Text(string="Description")

    state = fields.Selection(string="State", selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ], default='draft')

    def btn_draft(self):
        self.state = 'draft'

    def btn_confirm(self):
        self.state = 'confirm'

    def btn_cancel(self):
        self.state = 'cancel'