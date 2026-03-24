import base64
import os

from odoo import models, _
from odoo.modules.module import get_module_resource
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _get_icon_mapping(self):
        """ Dictionary: module technical name → icon filename (without .png extension) """
        return {
            'account': 'accounting',
            'account_accountant': 'accounting',
            'crm': 'crm',
            'documents': 'documents',
            'equity': 'equity',
            'hr': 'hr',
            'hr_expense': 'expenses',
            'stock': 'inventory',
            'mrp': 'manufacturing',
            'mass_mailing': 'mass_mailing',
            'point_of_sale': 'point_of_sale',
            'pos_restaurant': 'pos_restaurant',
            'project': 'project',
            'purchase': 'purchase',
            'sale_management': 'sale_management',
            'web_studio': 'studio',
            'timesheet_grid': 'timesheet_grid',
            'website': 'website',
            # ────────────────────────────────────────────────────────────────
            # Add your own entries here, example:
            # 'hr_recruitment': 'recruitment',
            # 'fleet': 'fleet',
            # 'mail': 'mail',
            # 'event': 'event',
            # etc.
        }

    def action_apply_custom_app_icons(self):
        """ Apply custom icons to root app menus based on mapping """
        self.ensure_one()

        mapping = self._get_icon_mapping()
        module_name = 'rebrand_app_icons'
        icon_folder = 'icons'
        updated_count = 0

        for mod_name, file_base in mapping.items():
            icon_path = get_module_resource(module_name, icon_folder, f"{file_base}.png")

            if not icon_path or not os.path.exists(icon_path):
                continue  # skip if file is missing

            with open(icon_path, 'rb') as f:
                icon_data = base64.b64encode(f.read())

            # Find root menus linked to this module
            menus = self.env['ir.ui.menu'].search([
                ('parent_id', '=', False),
                ('module', '=', mod_name),
            ])

            # Fallback: name contains module name (cleaned)
            if not menus:
                clean_name = mod_name.replace('_', ' ').title()
                menus = self.env['ir.ui.menu'].search([
                    ('parent_id', '=', False),
                    ('name', 'ilike', clean_name),
                ])

            # Another fallback: action model contains module
            if not menus:
                menus = self.env['ir.ui.menu'].search([
                    ('parent_id', '=', False),
                    ('action.res_model', 'ilike', mod_name.replace('_', '.')),
                ])

            if menus:
                menus.write({
                    'web_icon_data': icon_data,
                    'web_icon': False,  # disable original path-based icon
                })
                updated_count += len(menus)

        if updated_count == 0:
            raise UserError(_(
                "No icons were applied.\n\n"
                "Possible reasons:\n"
                "• PNG files missing in static/icons/\n"
                "• File names do not match the mapping dictionary\n"
                "• Developer mode not active\n"
                "• Restart Odoo server and hard-refresh browser (Ctrl+Shift+R)"
            ))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('%s app icons updated successfully.\nPlease reload the page.') % updated_count,
                'type': 'success',
                'sticky': False,
            }
        } | {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }