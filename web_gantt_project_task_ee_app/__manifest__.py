# -*- coding: utf-8 -*-
{
    'name': 'Web Gantt View for Project Task(Odoo Enterprise)',
    "author": "Edge Technologies",
    'version': '11.0.1.0',
    'live_test_url': "https://youtu.be/IAmN3_-VNVI",
    "images":['static/description/main_screenshot.png'],
    'summary': " This apps helps user to view web gantt view for project task in Half day, quarter day, half year and quarter year.",
    "description": """
                    Web Gantt view for Project , gantt view for project project gantt view ganttview pms gantt view task gantt view odoo gant view project gantview odoo project gantview odoo project gantview odoo project web gantt view view in gantt chart gantt chart pms project task gantt view projact task ganttview project web ganttview task project task web ganttview chart task gantt view chart  odoo web gantt chart 


                """,
    "license" : "OPL-1",
    'depends': ['base','web_gantt','project'],
    'data': [
            'views/web_gantt_project_task_app_view.xml',
            'views/web_gantt_templates.xml',
            ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 000,
    'currency': "EUR",
    'category': 'Projects',

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
