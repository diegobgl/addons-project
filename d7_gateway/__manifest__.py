# -*- coding: utf-8 -*-
{
    'name': "D7 SMS Gateway",

    'summary': """
        D7 SMS Gateway""",

    'description': """
        Act as a SMS gateway in Odoo for sending SMS from each modules
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list.for
    # The x.y.z version numbers follow the semantics breaking.feature.fix:
    #     x increments when the data model or the views had significant changes. Data migration might be needed,
    #       or depending modules might be affected.
    #     y increments when non-breaking new features are added. A module upgrade will probably be needed.
    #     z increments when bugfixes were made. Usually a server restart is needed for the fixes to be made available.


    'author': "Direct7 Networks",
    'website': "http://www.d7networks.com",
    'category': 'Tools',
    'version': '11.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base_setup',
    ],

    # always loaded
    'data': [
        'security/sms_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/res_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'images': ["static/description/banner.png"],
    'application': True,
}