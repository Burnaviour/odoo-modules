# -*- coding: utf-8 -*-
{
    "name": "Update Contact KKN",
    "summary": """
       This Module upgrade the Contact Module""",
    "description": """
        This Module upgrade the Contact Module
        Add Menu of District in Configuration open District Form from this menu
        Add Menu of Region in Configuration open District Form from this menu
        Add Menu of Station in Configuration open District Form from this menu
        Add Menu of Tier in Configuration open District Form from this menu
        KKN Development Team:
            Muhammad Tayyab <
            Muhammad Muzafar <
            Muhammad Husnain <
            
            
    """,
    "authors": "KKN Developers",
    "website": "https://www.kknetworks.com.pk",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Contact",
    "version": "16.0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "contacts"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/res_district.xml",
        "views/res_region.xml",
        "views/res_tier.xml",
        "views/res_station.xml",
        "views/res_partner.xml",
        "data/data.xml",
    ],
}
