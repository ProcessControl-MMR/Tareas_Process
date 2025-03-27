from odoo import models,fields, api


class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project template'

    name = fields.Char('Template name', required=True)

    task_template_ids = fields.Many2many('task.template', string='Task templates')
