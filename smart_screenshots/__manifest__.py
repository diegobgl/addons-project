# -*- coding: utf-8 -*-
{
    'name': "Project Task Screenshot",
    'summary': """Attach screenshots to the task.""",
    'author': "Kochyn's Band",
    'website': "https://github.com/kochyns-band/odoo_task_screenshot",
    'category': 'Project',
    'version': '11.0.1.0.1',

    'depends': [
        'base',
        'project',
        'web',
    ],
    'qweb': [
        'static/src/xml/screenshot.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/project_screenshot_settings.xml',
        'views/project_task_screenshot.xml',
        'views/project_task.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    "application": False,
}
