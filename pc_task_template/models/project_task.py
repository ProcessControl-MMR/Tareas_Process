from odoo import models, fields, api


class Task(models.Model):
    _inherit= 'project.task'

    task_template_id = fields.Many2one(
        'task.template',
        string='Task templates',
        help="Select a template for this task",
        domain="[('parent_id', '=', False)]"  # Excluye subtareas, solo muestra tareas principales
    )

    @api.model
    def create(self, vals):
        task = super(Task, self).create(vals)

        # Se comprueba si se ha seleccionado una plantilla de tarea
        if vals.get('task_template_id'):
            template = self.env['task.template'].browse(vals['task_template_id'])

            # Actualizar la tarea principal con los valores de la plantilla
            if template:
                # Name
                if not vals.get('name'):
                    name = template.name
                else:
                    name = vals.get('name')

                # Description
                if not vals.get('description'):
                    description = template.description
                else:
                    description = vals.get('description')

                # Responsible
                if not vals.get('responsible'):
                    responsible = template.responsible_id_default
                else:
                    responsible = vals.get('responsible')

                # Estimated deadline
                if not vals.get('date_deadline'):
                    deadline = self.env['task.template'].get_datetime_from_interval(template.interval_number, template.interval_type)
                else:
                    deadline = vals.get('date_deadline')

                task.name = name
                task.description = description
                task.user_ids = responsible
                task.date_deadline = deadline
                # task.task_category = template.task_category

            sub_templates = template.child_ids

            if sub_templates:
                for sub_template in sub_templates:
                    deadline = self.env['task.template'].get_datetime_from_interval(sub_template.interval_number,
                                                                                    sub_template.interval_type)
                    # Para cada subplantilla, creamos una nueva tarea
                    subtask_vals = {
                        'task_template_id': sub_template.id,
                        'parent_id': task.id,  # Vinculamos la subtarea a la tarea principal
                        'name': sub_template.name,
                        'description': sub_template.description,
                        'date_deadline': deadline,
                        'user_ids': [(4,
                                      sub_template.responsible_id_default.id)] if sub_template.responsible_id_default else False,
                    }

                    self.create(subtask_vals)
        return task


