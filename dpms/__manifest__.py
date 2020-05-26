# -*- coding: utf-8 -*-
{
    'name': "Project Management System",
    'license': 'LGPL-3',
    'support': "lyasine@3t-solutions.us",

    'summary': """
        This module allows managing, following up enterprise projects
        """,

    'description': """
       Project Management application for small and medium size businesses.
    """,

    'author': "3T Solutions LLC",
    'website': "http://www.3t-solutions.us",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project Management',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/phases_views.xml',
        'views/projecttype_views.xml',
        'views/risk_view.xml',
        'views/issues_views.xml',
        'views/tiers_view.xml',
        'views/program_views.xml',
        'views/programmanager_views.xml',
        'views/documenttemplate_views.xml',
        'views/change_history_views.xml',
        'views/project_export_wizard.xml',
        'reports/project_report.xml',
        'reports/project_planning_report.xml',
        'reports/project_details_report.xml',
        'reports/project_enhanced_report.xml',
        'views/main_menu.xml',
        'views/sequences.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application' : True,
    'installable' : True
}
