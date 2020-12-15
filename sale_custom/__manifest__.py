# -*- coding: utf-8 -*-
{
    'name': "Sale Custom",

    'summary': """""",

    'description': """
        Long description of module's purpose
    """,

    'author': "hieutrung15",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_custom_view.xml',
        'data/ex_xml.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
