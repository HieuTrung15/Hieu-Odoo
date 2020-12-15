from odoo import models, fields, api


class ToDo(models.Model):
    _name = 'to.do'
    _rec_name = 'title'
    _description = 'Todo'
    title = fields.Char(string='Title', required=True)
    description = fields.Html(string='Description')
    progress_state = fields.Selection([('todo', 'To do'),
                                       ('progress', 'In progress'),
                                       ('done', 'Done')],string='State', default='todo')

    def set_done(self):
        self.write({'progress_state': 'done'})