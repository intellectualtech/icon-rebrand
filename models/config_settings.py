import base64
import os
from odoo import models, _
from odoo.exceptions import AccessError, UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _get_icon_mapping(self):
        """ module_name → your actual icon filename (without .png) """
        return {
            'sale_management': 'sales',
            'crm': 'crm',
            'stock': 'inventory',
            'account': 'accounting',
            'purchase': 'purchase',
            'point_of_sale': 'point_of_sale',
            'pos_restaurant': 'kitchen_display',        # or 'point_of_sale'
            'project': 'projects',                      # you have "projects .png" and "projects (1).png"
            'mrp': 'manufacturing',
            'hr': 'employee',
            'hr_expense': 'expenses',
            'website': 'website',
            'documents': 'documents',
            'web_studio': 'apps',                       # or 'dashboard'
            'mass_mailing': 'email_marketing',
            'equity': 'accounting',                     # fallback
            'timesheet_grid': 'timesheets',
            'appointment': 'appointment',
            'recruitment': 'recruitment',
            'maintenance': 'maintenance',
            'field_service': 'field_service',
        }

    def action_apply_custom_app_icons(self):
        self.ensure_one()
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can apply custom app icons."))

        mapping = self._get_icon_mapping()
        module_root = os.path.dirname(os.path.dirname(__file__))
        icons_root = os.path.join(module_root, 'static', 'icons')
        updated_count = 0
        module_count = 0

        for mod_name, file_base in mapping.items():
            icon_path = os.path.join(icons_root, f"{file_base}.png")
            if not os.path.exists(icon_path):
                continue

            with open(icon_path, 'rb') as f:
                icon_data = base64.b64encode(f.read())

            modules = self.env['ir.module.module'].sudo().search([
                ('name', '=', mod_name),
            ])
            if modules:
                modules.write({'icon_image': icon_data})
                module_count += len(modules)

            menus = self.env['ir.ui.menu']

            # Prefer menu ids registered from the target module.
            menu_data = self.env['ir.model.data'].search([
                ('model', '=', 'ir.ui.menu'),
                ('module', '=', mod_name),
            ])
            if menu_data:
                menus = self.env['ir.ui.menu'].browse(menu_data.mapped('res_id')).filtered(
                    lambda m: not m.parent_id
                )

            if not menus:
                menus = self.env['ir.ui.menu'].search([
                    ('parent_id', '=', False),
                    ('module', '=', mod_name),
                ])

            if not menus:
                menus = self.env['ir.ui.menu'].search([
                    ('parent_id', '=', False),
                    ('name', 'ilike', mod_name.replace('_', ' ').title()),
                ])

            if menus:
                menus.write({
                    'web_icon_data': icon_data,
                    'web_icon': False,
                })
                updated_count += len(menus)

        if updated_count == 0 and module_count == 0:
            raise UserError(_("No icons applied.\nMake sure your PNG files exist in static/icons/ and match the configured mapping."))

        self.env.registry.clear_cache()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Icons Updated"),
                'message': _("Updated %(modules)s app definitions and %(menus)s installed app menus.", modules=module_count, menus=updated_count),
                'type': 'success',
                'sticky': False,
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                },
            },
        }