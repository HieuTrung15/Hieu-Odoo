# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# nhung thong tin co ban cua 1 module
{
    'name': 'First Module',
    'version': '1.0',
    'summary': 'day la tom tat',
    'sequence': 10,
    'description': """  Mo ta module 
    """,
    'author': 'hieutrung15',
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/',
    'depends': ['base', 'mymodules'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_employee_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
