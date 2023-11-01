# -*- coding: utf-8 -*-
{
    "name": "Fuel",
    "summary": """
        Fuel module used to assign fuel card to employee""",
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
    "depends": ["base", "hr", "mail"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/assign_fuel_card.xml",
        "views/menu.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
}
