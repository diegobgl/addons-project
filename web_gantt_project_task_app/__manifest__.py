# -*- coding: utf-8 -*-

{
    "name" : "Web Gantt View for Project Task in Odoo Community",
    "author": "Edge Technologies",
    "version" : "11.0.1.0",
    "live_test_url":'https://www.youtube.com/watch?v=1HQwcQ037bI',
    "images":["static/description/main_screenshot.png"],
    'summary': "This apps helps user to view web gantt view for project task in quarter day and half day.",
    "description": """
                    Web Gantt view for Project , gantt view for project project gantt view ganttview pms gantt view task gantt view odoo gant view project gantview odoo project gantview odoo project gantview odoo project web gantt view view in gantt chart gantt chart pms project task gantt view projact task ganttview project web ganttview task project task web ganttview chart task gantt view chart  odoo web gantt chart 


                """,
    "license" : "OPL-1",
    "depends" : ['web', 'project'],
    "data": [
            'views/web_gantt_templates.xml',
            'views/web_gantt_project_task_app_view.xml',
            ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    "auto_install": False,
    "installable": True,
    "price": 000,
    "currency": 'EUR',
    "category" : "Project",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
