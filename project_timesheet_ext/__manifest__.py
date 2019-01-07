# -*- coding: utf-8 -*-
{
    "name": """Timesheet Action Button""",
    "summary": """Timesheet Action""",
    "category": "Project",
    "images": ['static/description/icon.png'],
    "version": "11.18.5.16.0",
    "description": """
       
    """,
    "author": "Viktor Vorobjov",
    "license": "OPL-1",
    "website": "https://straga.github.io",
    "support": "vostraga@gmail.com",

    "depends": [
        "project",
        "hr_timesheet",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/hr_timesheet_view.xml',
    ],
    "qweb": [],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}