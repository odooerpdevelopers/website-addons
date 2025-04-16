{
    'name': 'Ejemplo de Eventos OWL',
    'version': '1.0',
    'summary': 'Ejemplo para demostrar la comunicación padre-hijo con eventos en OWL',
    'category': 'Website',
    'author': 'OdooErpCloud',
    'website': 'https://odooerpcloud.com',
    'license': 'AGPL-3',
    'depends': ['web'],
    'data': [
        'views/server_templates.xml',  # Para el template que lanza el componente
    ],
    'assets': {
        'web.assets_frontend': [
            'owl_events/static/src/components/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}