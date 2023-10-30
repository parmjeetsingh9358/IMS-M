# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = "res.users"

    incident_partner_ids = fields.One2many("incident.register.partner", "user_id")
