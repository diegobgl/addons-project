# -*- coding: utf-8 -*-

{
    'name': "Project Stages",
    'version' : '0.1',
    'author' : 'T.V.T Marine Automation (aka TVTMA)',
    'website': 'https://www.tvtmarine.com',
    'live_test_url': 'https://v11demo-int.erponline.vn',
    'support': 'support@ma.tvtmarine.com',
    'summary': 'Configure project stages',
    'category' : 'Project',
    'sequence': 11,
    'description': """
This is a simple application that changes the project form view for the users to organise stages specific to projects
    
Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_stages_view.xml',

    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',
    'license': 'OPL-1',
}
