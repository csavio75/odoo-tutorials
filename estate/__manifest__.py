{
    'name': "Real Estate",
    'version': '1.0',
    'author': "Charlot Raveloarison",
    'category': 'Tutorials/Estate',
    'description': """
    Real estate with odoo tutorials
    """,
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ]
}
