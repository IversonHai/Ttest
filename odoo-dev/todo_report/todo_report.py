from openerp import models, fields

class TodoReport(models.Model):
    _name = 'todo.task.report'
    _description = 'To-do Report'
    _sql = """
        CREATE OR REPLACE VIEW todo_task_report AS
        select *
        from todo_task
        where active = TRUE 
        """
    name = fields.Char('Description')
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?')
    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')