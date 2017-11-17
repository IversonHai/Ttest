# -*- coding: utf-8 -*
from openerp import models, fields

class TodoTask(models.Model):
    _inherit = 'todo.task'
    color = fields.Integer('Color Index')
    priority = fields.Selection([('1', 'very Low'),
                                 ('2', 'Low'),
                                 ('3', 'Normal'),
                                 ('4', 'High'),
                                 ('5', 'very High')],
                                'Priority', default='1')
    kanban_state = fields.Selection([('normal', 'In Progress'),
                                     ('blocked', 'Blocked'),
                                     ('done', 'Ready for next stage')],
                                    'Kanban State', default='normal')