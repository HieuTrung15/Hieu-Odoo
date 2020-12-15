# from odoo import models, fields
from odoo import api, fields, models, tools, _
# from odoo.exceptions import UserError, ValidationError


class ShowModel(models.Model):
    _name = 'show.model'
    name = fields.Char('Name', required=True)
    # def _default_name(self):
    #     return self.get_value()
    #
    # name = fields.Char(default=lambda self: self._default_name())
    name_upper = fields.Char(string='Name_Upper', compute="_compute_name_upper", inverse="_inverse_upper_name", store=True,
                             search='_search_upper')
    age = fields.Integer('Age', default=10)
    gender = fields.Char('Gioi tinh', default='Nam')
    date_of_birth = fields.Date('Ngay sinh')
    address = fields.Char('Address')

    @api.depends('name')
    def _compute_name_upper(self):
        for rec in self:
            rec.name_upper = rec.name.upper() if rec.name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.name = rec.name_upper.lower() if rec.name_upper else False

    def _search_upper(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return [('name', operator, value)]

