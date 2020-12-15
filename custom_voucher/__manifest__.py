# -*- coding: utf-8 -*-
{
    'name': "Voucher",
    'summary': """Voucher Management""",
    'description': """Voucher ....""",
    'author': "Light",
    'website': "",
    'category': '',
    'version': '0.1',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/voucher_data.xml',
        'views/voucher_program.xml',
        'wizard/apply_voucher.xml',
        'views/voucher.xml',
        'views/sale_order.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}
