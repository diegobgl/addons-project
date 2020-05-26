# Copyright 2013-Today Seven Gates Interactive Technologies

{
    'name': 'Project Default Stage',
    'summary': 'Adds default stage, which are defined in stages, to the projects.',
    'description': '''
This module offers default stages for projects. If enabled while creating a stage and a project, 
the module creates all the default stages when on project creation.''',
    'author': 'SevenGates Interactive Technologies',
    'version': '11.0.1.0.0',
    'category': 'Project',
    'website': 'https://www.sevengates.co',
    'depends': [
        'base',
        'project',
    ],
    'data': [
        'views/project_default_stage.xml',
    ],
    'installable': True,
    'application': False,
    'css': ['static/src/css/project_default_stage_7g.css'],
    'images': ["images/main_screenshot.png",
               "static/description/icon.png"],
    'license': 'OPL-1',
    'support': 'support@sevengates.co',
    'price': 0.0,
    'currency': 'EUR',
}
