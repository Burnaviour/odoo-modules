{
    'name': "POP",

    'summary': """

        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "application": True,
    "sequence": -400,
    "version": "0.1",
    # any module necessary for this one to work correctly

    "depends": [
        "base",
        "mail",
        "stock",
        "update_contact_kkn",
        "account",
        "uom",
        "update_inventory_kkn",
        "base_geolocalize",
    ],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/menus.xml",
        "views/views.xml",
        "views/add_pop.xml",
        "views/edit_pop.xml",
        "views/close_pop.xml",
        "views/all_pop.xml",
        "reports/report.xml",
        "reports/all_reports.xml",
        "reports/monthly_pop_rent_bill_report.xml",
        "wizards/monthly_pop_rent_bill_report_wiz.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
}
# -*- coding: utf-8 -*-
