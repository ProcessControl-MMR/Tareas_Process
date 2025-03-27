from odoo import models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    project_template_id = fields.Many2one('project.template', string='Project template', help="Select a template for this project")

    @api.model
    def create(self, vals):
        # Creación del proyecto principal
        project = super(Project, self).create(vals)

        # Aquí verificamos si se ha seleccionado una plantilla
        project_template = self.env['project.template'].browse(vals.get('project_template_id'))

        if project_template:
            # Si se ha seleccionado una plantilla, aplicamos los valores de la plantilla
            project.name = project_template.name

            # Crear tareas desde las plantillas de tareas asociadas, si existen
            if project_template.task_template_ids:
                for task_template in project_template.task_template_ids:
                    # Verificar si la tarea ya existe para este proyecto (por nombre o alguna otra condición)
                    existing_task = self.env['project.task'].search([
                        ('project_id', '=', project.id),
                        ('name', '=', task_template.name)
                    ], limit=1)

                    if not existing_task:
                        # Crear una tarea sólo si no existe ya para el proyecto
                        task_vals = {
                            'task_template_id': task_template.id,
                            'name': task_template.name,
                            'project_id': project.id,
                            'description': task_template.description,
                            'user_ids': [(4,
                                          task_template.responsible_id_default.id)] if task_template.responsible_id_default else [],
                            'date_deadline': task_template.deadline,
                        }
                        task = self.env['project.task'].create(task_vals)

                        # Crear subtareas si existen
                        if task_template.child_ids:
                            for subtask_template in task_template.child_ids:
                                # Verificar si la subtarea ya existe para la tarea
                                existing_subtask = self.env['project.task'].search([
                                    ('parent_id', '=', task.id),
                                    ('name', '=', subtask_template.name)
                                ], limit=1)

                                if not existing_subtask:
                                    # Crear la subtarea solo si no existe
                                    subtask_vals = {
                                        'task_template_id': subtask_template.id,
                                        'parent_id': task.id,  # Vinculamos la subtarea con la tarea principal
                                        'name': subtask_template.name,
                                        'description': subtask_template.description,
                                        'user_ids': [(4,
                                                      subtask_template.responsible_id_default.id)] if subtask_template.responsible_id_default else False,
                                        'date_deadline': subtask_template.deadline,
                                    }
                                    self.env['project.task'].create(subtask_vals)

        return project

