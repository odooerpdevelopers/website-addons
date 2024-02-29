{
    'name': 'Widget Form',
    'version': '1.1',
    'summary': 'JS Widgets, Forms for Odoo Website',
    'description': """
    Widgets in Odoo
    This app enables you to bind JavaScript widgets to forms on websites from scratch.
    """,
    'category': 'Custom',
    'author': 'odooexperto.com',
    'website': 'https://odooexperto.com',
    'license': 'AGPL-3',
    'depends': ['base', 'portal',  'web', 'website'],
    'data': [
        'views/templates.xml'
    ],

    'installable': True,
    'auto_install': False,
}
