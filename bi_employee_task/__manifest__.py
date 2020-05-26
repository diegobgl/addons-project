# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Project Tasks',
    'version': '11.0.0.1',
    'author': 'BrowseInfo',
    "category": "Human Resources",
    "description": """
        This module helps to display assinged task to Employee, employee tasks, tasks employee,visible tasks on employee. Tasks list on employee,
    """,
    'license':'OPL-1',
    'summary': 'This module helps to display assinged task to Employee form and kanban view',
    'website': 'www.browseinfo.in',
    'description':""" """, 
    'depends':['base','hr','project'],
    'data':[
        'views/employee_task.xml',
        'security/employee_security.xml',
        ],
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

