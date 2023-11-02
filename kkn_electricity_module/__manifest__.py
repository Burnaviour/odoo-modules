# -*- coding: utf-8 -*-
{
    'name': "Electricity",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'application': True,
    'sequence': -500,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product','update_contact_kkn', 'kkn_pop_module', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/menu.xml',
        'views/views.xml',
        'views/assign_electricity_meters.xml',
        'views/bill_electricity_meters.xml',
        'views/electricity_meters.xml',
        'wizard/monthly_electricity_bills_report_wiz.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',

}
