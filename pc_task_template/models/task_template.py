from odoo import models,fields
from dateutil.relativedelta import relativedelta


class TaskTemplate(models.Model):
    _name = 'task.template'
    _description = 'Task templates'

    name = fields.Char('Task name', required=True)
    description = fields.Html('Description')
    # Cada plantilla de tarea está asociada con uno o muchos proyectos
    project_id = fields.Many2one('project.project', 'Target project', required=False)
    responsible_id_default = fields.Many2one('res.users', 'Responsible by default', required=False)
    task_category = fields.Text('Task type')
    # task_category_id = fields.Many2one('project.task', 'Tipo de Tarea', required=False)
    parent_id = fields.Many2one('task.template', string='Parent template', index=True,
                                domain="[('parent_id', '=', False)]")
    child_ids = fields.Many2many('task.template', 'task_template_relation', 'task_id', 'related_task_id', string="Sub-templates")

    task_ids = fields.Many2many('project.task', string='Task')

    # Diccionario que define los intervalos de tiempo
    _intervalTypes = {
        'days': lambda interval: relativedelta(days=interval),
        'hours': lambda interval: relativedelta(hours=interval),
        'weeks': lambda interval: relativedelta(days=7 * interval),
        'months': lambda interval: relativedelta(months=interval),
        'minutes': lambda interval: relativedelta(minutes=interval),
    }

    interval_number = fields.Integer(default=1, string="Estimated term", help="Estimated time for completion of the task")
    interval_type = fields.Selection([('days', 'Days'),
                                      ('weeks', 'Weeks'),
                                      ('months', 'Months')], string='Interval Unit', default='months')


    def get_datetime_from_interval(self, interval_number=1, interval_type='months'):

        interval = self._intervalTypes.get(interval_type, lambda x: relativedelta(days=0))(interval_number)
        deadline = fields.Datetime.to_string(fields.Date.today() + interval)
        return deadline


