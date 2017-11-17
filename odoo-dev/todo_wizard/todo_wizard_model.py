# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions  # will be used in the code
import logging

_logger = logging.getLogger(__name__)

_logger.debug('A DEBUG message')
_logger.info('An INFO message')
_logger.warning('A WARNING message')
_logger.error('An ERROR message')


class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    task_ids = fields.Many2many('todo.task', string='Tasks')
    new_deadline = fields.Date('Deadline to Set')
    new_user_id = fields.Many2one('res.users', string='Responsible to Set')

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise exceptions.ValidationError('No data to update!')
            # else:
        _logger.debug('Mass update on Todo Tasks %s',
                      self.task_ids.ids)
        if self.new_deadline:
            self.task_ids.write({'date_deadline': self.new_deadline})
        if self.new_user_id:
            self.task_ids.write({'user_id': self.new_user_id.id})
        return True

    @api.multi
    def do_count_tasks(self):
        Task = self.env['todo.task']
        count = Task.search_count([('is_done', '=', False)])
        raise exceptions.Warning('There are %d active tasks.' % count)

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def do_populate_tasks(self):
        self.ensure_one()
        Task = self.env['todo.task']
        open_tasks = Task.search([('is_done', '=', False)])
        self.task_ids = open_tasks
        return self._reopen_form()

    @api.multi
    def do_get_lins(self):
        ids = self.env.context.get('active_ids')
        lins = self.env['todo.task'].browse(ids)
        self.task_ids = lins
        return self._reopen_form()