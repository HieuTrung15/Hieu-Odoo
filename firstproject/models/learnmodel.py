from odoo import models, fields, api
from datetime import datetime


class ResEmployee(models.Model):
    _name = 'res.employee'
    name = fields.Char('Name')
    date_of_birth = fields.Datetime('Date of birth')
    address = fields.Char('Address')


class InheritResEmployee(models.Model):
    _inherit = 'res.employee'

    depend_field = fields.Char()

    age = fields.Integer(compute='compute_age')
    age_constrain = fields.Integer()

    @api.model
    def create(self, vals):
        res = super(InheritResEmployee, self).create(vals)
        return res

    @api.onchange('name')
    def onchange_name(self):
        if self.name == 'hieu':
            self.address = 'hung yen'
        else:
            self.address = 'Null'

    def compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                duration = datetime.now().year - rec.date_of_birth.year
                rec.age = duration
            else:
                rec.compute_fields = 0

    @api.constrains('date_of_birth')
    def constrains_age_constrain(self):
        if self.date_of_birth:
            duration = datetime.now().year - self.date_of_birth.year
            self.age_constrain = duration
        else:
            self.age_constrain = 0

    show_model_id = fields.Many2one('show.model')
    show_model_related = fields.Integer(related='show_model_id.age', readonly=0)

