{
    'name': "Rebrand App Icons - Custom per App/Module",
    'version': '18.0.1.0',
    'summary': 'Replace default dashboard app icons with custom PNGs per module',
    'description': """
        Full rebranding of the Odoo Apps dashboard icons.
        Place one PNG per app in static/icons/ (e.g. sale_management.png, crm.png, etc.)
        Click the button in Settings to apply changes to root menus.
    """,
    'author': "Your Company / David",
    'category': 'Technical',
    'depends': ['base'],
    'data': [
        'views/settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}