# -*- coding: utf-8 -*
from openerp import models, fields, api
class TodoTask(models.Model):
    _name = 'todo.task'
    name = fields.Char('Description_l', required=True)
    test = fields.Char('Test')
    title = fields.Char('Title')
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)
    test = fields.Char('test')
    stage_id = fields.Many2one('todo.task.test', 'Stage')

    @api.one
    def do_toggle_done(self):
        self.is_done = not self.is_done
        return True

    @api.multi
    def do_clear_done(self):
        done_recs = self.search([('is_done', '=', True)])
        done_recs.write({'active': False})
        return True

class Stage(models.Model):
   _name = 'todo.task.test'
   name = fields.Char(string='Name', translate=True)
   sequence = fields.Integer(string='Sequence')
   test_ids = fields.One2many('todo.task','stage_id')
   # qingjia_ids = fields.One2many('qingjia.qingjd','qingjia_id')


