from odoo import models,fields, api
from dateutil.relativedelta import relativedelta


class TaskTemplateWizard(models.TransientModel):
    _name = 'task.template.wizard'
    _description = 'Wizard to create tasks from a template'

    responsible_id_default = fields.Many2one('res.users', 'Responsible by default', required=False)
    task_template_id = fields.Many2one('task.template',
                                       'Task template', required=True,
                                       help="Select a template to create the task",
                                       domain="[('parent_id', '=', False)]")

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

    @api.onchange('task_template_id')
    def _onchange_task_template(self):
        # Asignación responsable por defecto al seleccionar una plantilla de tareas
        if self.task_template_id:
            self.responsible_id_default = self.task_template_id.responsible_id_default or False
            self.interval_number = self.task_template_id.interval_number
            self.interval_type = self.task_template_id.interval_type

    def action_create_tasks(self):
        # Obtenemos el ID del proyecto desde donde se está invocando el wizard
        project_id = self.env.context.get('active_id')

        # Calculamos la fecha de la próxima ejecución
        if self.interval_number and self.interval_type:
            deadline = self.env['task.template'].get_datetime_from_interval (self.interval_number, self.interval_type)
        else:
            # Si no se ha indicado un intervalo, usamos la fecha de la plantilla
            deadline = self.env['task.template'].get_datetime_from_interval (self.task_template_id.interval_number,
                                                                             self.task_template_id.interval_type)

        # Crear la tarea de la plantilla seleccionada
        vals = {
            'project_id': project_id,
            'task_template_id': self.task_template_id.id,
            'name': self.task_template_id.name,
            'description': self.task_template_id.description,
            'date_deadline': deadline,
            'user_ids': [(4,
                          self.responsible_id_default.id)] if self.responsible_id_default else False,
        }

        self.env['project.task'].create(vals)
