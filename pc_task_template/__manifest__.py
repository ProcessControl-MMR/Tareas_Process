# -*- coding: utf-8 -*-
{
    'name': "Pc task template",
    'summary': "Plantilla de projectos, tareas y gestión de subtareas",
    'author': "Process Control",
    'website': "https://www.processcontrol.es/",
    'category': 'Project',
    'version': '17.0.0.0.1',
    "license": "AGPL-3",
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/task_template_views.xml',
        'views/project_task_views.xml',
        'views/project_template_views.xml',
        'wizard/task_template_wizard_views.xml'

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}


