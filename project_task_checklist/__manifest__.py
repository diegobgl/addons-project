# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': "Project Task Checklist",
    'version': "11.0.1.2.10",
    'category': "Project",
    'sequence': 10,
    'summary': "Add checklist to project task",
    'license': 'LGPL-3',
    'author': "Fenix Engineering Solutions",
    'website': "http://www.fenix-es.com",
    'images': [
        'static/description/cover.png'
    ],
    'depends': ['project', ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/project_inherit.xml',
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
