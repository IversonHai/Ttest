# -*- coding: utf-8 -*
from openerp import models, fields, api
class TodoTask(models.Model):
    #_inherit类属性是这里的关键：它告诉Odoo这个类继承自todo.task模型。
    #  注意_name属性不存在。 它不是必需的，因为它已经从父模型继承。
    #_inherit = 'todo.task'

    # 本次对todo.task模型的扩展是通过将这个模型复制mail.thread模型的功能而实现的。
    # mail.thread模型实现Odoo消息和关注人功能，而且是可以被重复使用的，
    # 因此，我们可以很轻松地将这些功能添加任何一个模型
    _name = 'todo.task'
    # 运用继承添加社交网络功能
    _inherit = ['todo.task', 'mail.thread']
    name = fields.Char(help="What needs to be done?")

    #user_id表示用户模型中的用户res.users。 它是一个Many2one字段，相当于数据库术语中的外键。
    user_id = fields.Many2one('res.users', 'Responsible')

    #date_deadline是一个简单的日期字段。
    date_deadline = fields.Date('Deadline')


@api.multi
def do_clear_done(self):
    domain = [('is_done', '=', True),
              '|', ('user_id', '=', self.env.uid),
              ('user_id', '=', False)]
    done_recs = self.search(domain)
    done_recs.write({'active': False})
    return True

@api.one
def do_toggle_done(self):
    if self.user_id != self.env.user:
        raise Exception('Only the responsible can do this!')
    else:
        return super(TodoTask, self).do_toggle_done()