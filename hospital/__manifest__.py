# -*- coding: utf-8 -*-
{
    'name': "hospital",

    'summary': """
        Hospital Management System """,

    'description': """
       Hospital Management Module to manage hospital Records 
    """,
    'auto_install': False,
    'author': "Burnaviour",
    'website': "https://www.kkn.com",

    # Categories can be used to filter modules in modules listing1
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HOSPITAL Management',
    "license": "LGPL-3",
    'version': '10.0.0',
    'application': True,
    'sequence': -100,
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'data/patient.tag.csv',
        'data/patient_tag_data.xml',
        'data/sequence_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/views.xml', 'views/menu.xml',
        'views/patient_data.xml',
        'views/appointment_view.xml',
        'views/templates.xml',
        'views/female_patients_data.xml',
        'views/patient_tag_view.xml',
        'views/playground_view.xml',
        'views/operation_view.xml',
        # 'views/res_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]

}
