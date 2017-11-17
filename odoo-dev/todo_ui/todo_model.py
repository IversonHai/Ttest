# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.addons.base.res import res_request

class Tags(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True

    # _parent_name = 'parent_id'
    name = fields.Char('Name1')
    parent_id = fields.Many2one('todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    advert_attachment = fields.Many2one('ir.attachment', string=u'广告视频')
    task_ids = fields.Many2many('todo.task', string='Tasks')

class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'

    # String fields:
    name = fields.Char('Name')
    desc = fields.Text('Description')
    state = fields.Selection([('draft', 'New'), ('open', 'Started'), ('done', 'Closed')],'State')
    docs = fields.Html('Documentation')
    # Numeric fields:
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete', (3, 2))
    # Date fields:
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Changed')
    # Other fields:
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')
    tasks = fields.One2many('todo.task',  # related model
                             'stage_id',  # field for "this" on related model
                            'Tasks')

    @api.constrains('name')
    def _check_name_size(self):
        for task in self:
            if len(task.name) < 5:
                raise ValidationError('The name Must have 5 chars!')

    @api.onchange('date_changed')
    def _onchang_desc(self):
        self.desc=self.date_changed

    _sql_constraints = [('date_check',
                         "CHECK('date_effective' ,'>=','date_changed')",
                         "开始日期必须大于结束日期")
                        ]

class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    refers_to = fields.Reference([('res.users', 'User'), ('res.partner', 'Partner')], 'Refers to')
    user_todo_count = fields.Integer('User To-Do Count', compute='compute_user_todo_count')
    effort_estimate = fields.Integer('effort estimate')

    # stage_fold = fields.Boolean('Stage Folded?', compute='_compute_stage_fold')
    stage_fold = fields.Boolean(string='Stage Folded?',
                                compute='_compute_stage_fold',
                                # store=False)  # the default
                                search='_search_stage_fold',
                                inverse='_write_stage_fold')

    stage_state = fields.Selection(related='stage_id.state',
                                   string='Stage State',
                                   store=True,
                                   inverse='_write_state')

    tag_ids = fields.Many2many(comodel_name='todo.task.tag',  # related model
                                relation='todo_task_tag_rel',  # relation table name
                                column1='task_id',  # field for "this" record
                                column2='tag_id',  # field for "other" record
                                string='Tags')

    _sql_constraints = [('todo_task_name_uniq',
                         'UNIQUE (name, user_id, active)',
                         'Task title must be unique!')]

    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count(
            [('user_id', '=', self.user_id.id)])


