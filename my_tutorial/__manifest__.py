{
    'name': 'My Tutorial',
    'version': '1.0',
    'summary': 'day la tom tat',
    'sequence': 10,
    'description': """  Mo ta module 
    """,
    'author': 'hieutrung15',
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/my_tutorial_view.xml',
        'views/my_student_view.xml',
        'views/menu_item_view.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
