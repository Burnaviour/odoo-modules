# -*- coding: utf-8 -*-
{
    'name': "Update Location Form",

    'summary': """
        Generate Unique ID, Add pop type and locate latitude and longitude""",

    'description': """
        -  Show City code before unqiue id  
        -  Generate Location ID according to selected city automatically for every form
        -  Add new type pop in location form
        -  Add new page in Location form
        -  Automatically find latitude and longitude according to given addresses
    """,

    'author': "Muhammad Hasnain",
    'website': "http://www.kknetworks.com.pk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'contacts', 'sale', 'update_contact_kkn', 'base_geolocalize'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/update_contact_stock_location_view.xml',
    ],
}
