# Rebrand Icons (Odoo 19)

This module applies custom PNG icons to Odoo root app menus (dashboard tiles).

It covers both:

- Installed apps via `ir.ui.menu.web_icon_data`
- Not-yet-installed apps in Apps via `ir.module.module.icon_image`

## Requirements

- Odoo 19 (on-premise)
- Module directory name: `icon_rebrand`
- Icons stored in `static/icons/*.png`

## Install (On-Premise)

1. Put the module in your custom addons path.
2. Ensure Odoo config includes that path in `addons_path`.
3. Restart Odoo service.
4. Enable Developer Mode.
5. Open Apps and click `Update Apps List`.
6. Search for `icon_rebrand` and click `Install`.

## Upgrade After Code Changes

1. Restart Odoo service.
2. Open Apps and search `icon_rebrand`.
3. Open module form and click `Upgrade`.

CLI alternative:

```bash
./odoo-bin -d <database_name> -u icon_rebrand --stop-after-init
```

## Usage

1. Go to Settings.
2. Open `Rebrand Icons` menu.
3. Click `Apply Custom Icons to Each App`.
4. Hard refresh browser (`Ctrl+Shift+R`).
5. If Apps icons are still cached, reload the Apps page after upgrade.

## Notes

- The module updates root menus (`ir.ui.menu`) icon fields.
- The module also updates app definitions (`ir.module.module.icon_image`) for apps not yet installed.
- Mapping is defined in `models/config_settings.py`.
- If no icon is applied, verify icon filenames and mapping keys.