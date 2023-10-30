# -*- coding: utf-8 -*-
{
    "name": "update_inventory_kkn",
    "summary": """
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
    "category": "Customizations",
    "version": "16.0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "views/product_template_view.xml",
        "views/switchport_view.xml",
        "views/update_contact_stock_location_view.xml",
        "views/update_location.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    'license': 'LGPL-3',

}
