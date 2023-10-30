# -*- coding: utf-8 -*-

from odoo import models, api, tools


class Menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        menus = super(Menu, self)._visible_menu_ids(debug)
        super_admin = self.user_has_groups('mysisco_incident_register.group_incident_register_super_admin')
        if not super_admin:
            for menu in [
                'base.menu_management',
                'spreadsheet_dashboard.spreadsheet_dashboard_menu_root',
                'calendar.mail_menu_calendar',
                'utm.menu_link_tracker_root',
                'mail.menu_root_discuss',
                'website.menu_website_preview',
                'website.menu_website_configuration',
            ]:
                menu_id = self.env.ref(menu)
                menus.discard(menu_id.id)
        else:
            if not self.user_has_groups("base.group_system"):
                for menu in [
                    'mysisco_incident_register.menu_incident_register_id',
                    'mysisco_incident_register.employees_incident_id',
                    'mysisco_incident_register.location_incident_id',
                    'mysisco_incident_register.other_admin_incident_id',
                ]:
                    menu_id = self.env.ref(menu)
                    menus.discard(menu_id.id)
        return menus
