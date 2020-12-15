from odoo import fields, models, api

class Student(models.Model):
    _name = 'my.student'

    name = fields.Char(string="Name")
    age = fields.Char(string="Age")
    address = fields.Char(string="Address")

    school_id = fields.Many2one(comodel_name='my.tutorial', string="School")

