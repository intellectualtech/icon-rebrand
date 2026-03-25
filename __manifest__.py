{
    'name': "Rebrand Icons - Custom per App (Odoo 19)",
    'version': '19.0.1.0.0',
    'summary': 'Replace default Odoo app icons with custom icons from static/icons folder',
    'description': 'Apply custom app icons from static/icons to root app menus from Settings.',
    'author': 'Intellectual Technology',
    'website': 'https://www.intellectualtechnology.com.na',
    'category': 'Tools',
    'depends': ['base', 'web'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'icon_rebrand/static/src/js/app_icon_override.js',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}