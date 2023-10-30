# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

from odoo import Command, _, fields, models, api
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_partner import now


class IncidentRegisterPartner(models.Model):
    _name = "incident.register.partner"
    _inherit = ['mail.activity.mixin', 'mail.thread.blacklist']
    _description = "Incident Register Partner"

    active = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner', tracking=True)
    name = fields.Char()
    state = fields.Selection(
        [('draft', "Pending"), ('posted', 'Invited')], default='draft', tracking=True, string="Status")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string="Country")
    incident_city_ids = fields.Many2many('incident.city', string="Locations")
    incident_role_id = fields.Many2one('incident.role', string="Incident Role")
    email = fields.Char(tracking=True, )
    phone = fields.Char(tracking=True, )
    mobile = fields.Char(tracking=True, )
    function = fields.Char(string='Job Position')
    website = fields.Char("Website", tracking=True)
    title = fields.Many2one('res.partner.title', tracking=True)
    company_partner_id = fields.Many2one('res.partner', string='Company', store=True)
    is_company_create = fields.Boolean()
    user_id = fields.Many2one('res.users', string="User")
    manager_id = fields.Many2one('incident.register.partner', string='Manager')
    is_manager = fields.Boolean()
    manager_role = fields.Boolean()
    new_incident_role_id = fields.Many2one('incident.role', string="New Incident Role",
                                           compute="_compute_new_incident_role_id")
    is_company = fields.Boolean()
    incident_image = fields.Image()
    manager_count = fields.Integer(string='Total Manager', compute='_compute_manager_count')
    staff_count = fields.Integer(string='Staff', compute='_compute_staff_count')
    location_count = fields.Integer(string='Location', compute='_compute_location_count')

    def _compute_manager_count(self):
        for rec in self:
            manager_role_id = self.env.ref("mysisco_incident_register.incident_role_manager").id
            manager_count = rec.search_count([('incident_role_id', '=', manager_role_id),('company_partner_id', '=', rec.company_partner_id.id)])
            rec.manager_count = manager_count
    def _compute_staff_count(self):
        for rec in self:
            staff_role_id = self.env.ref("mysisco_incident_register.incident_role_staff").id
            staff_count = rec.search_count([('incident_role_id', '=', staff_role_id), ('manager_id', '=', rec.id),('company_partner_id', '=', rec.company_partner_id.id)])
            rec.staff_count = staff_count
    def _compute_location_count(self):
        for rec in self:
            location = rec.env['incident.city'].search_count([('partner_id', '=', rec.company_partner_id.id)])
            rec.location_count = location

    def action_open_manager(self):
        manager_role_id = self.env.ref("mysisco_incident_register.incident_role_manager").id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'incident.register.partner',
            'name': 'Manager',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('incident_role_id', '=', manager_role_id),('company_partner_id', '=', self.company_partner_id.id)],
        }
    def action_open_staff(self):
        staff_role_id = self.env.ref("mysisco_incident_register.incident_role_staff").id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'incident.register.partner',
            'name': 'Staff',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('incident_role_id', '=', staff_role_id), ('company_partner_id', '=', self.company_partner_id.id)],
        }
    def action_open_location(self):
        action = self.env.ref("mysisco_incident_register.view_incident_action_location_id_for_emp").sudo().read()[0]
        action['domain'] = [('partner_id', '=', self.company_partner_id.id)]
        return action

    @api.depends("incident_role_id")
    def _compute_new_incident_role_id(self):
        admin_role_id = self.env.ref("mysisco_incident_register.incident_role_admin").id
        manager_role_id = self.env.ref("mysisco_incident_register.incident_role_manager").id
        staff_role_id = self.env.ref("mysisco_incident_register.incident_role_staff").id
        for rec in self:
            rec.is_manager = False
            if rec.incident_role_id.id == manager_role_id:
                manager_id = self.sudo().search([('user_id', '=', self.env.user.id)], limit=1)
                rec.new_incident_role_id = admin_role_id
                if not rec.manager_id:
                    rec.manager_id = manager_id.id
                rec.is_manager = True
                rec.manager_role = True
            elif rec.incident_role_id.id == staff_role_id:
                rec.new_incident_role_id = manager_role_id
                rec.is_manager = True
                rec.manager_role = False
            else:
                rec.new_incident_role_id = False
                rec.manager_role = False

    @api.model
    def default_get(self, fields):
        res = super(IncidentRegisterPartner, self).default_get(fields)
        admin = self.env.user.has_group('mysisco_incident_register.group_incident_register_admin')
        manager = self.env.user.has_group('mysisco_incident_register.group_incident_register_manager')
        incident_partner_id = self.sudo().search([('user_id', '=', self.env.user.id)], limit=1)
        if admin:
            res['is_company_create'] = True
            res['company_partner_id'] = incident_partner_id.company_partner_id.id or incident_partner_id.partner_id.id
        elif manager:
            res['is_company_create'] = True
            res["manager_id"] = incident_partner_id.id
            res['company_partner_id'] = incident_partner_id.company_partner_id.id
        return res

    def revoke_invitation(self):
        expiration = now(days=-1)
        self.mapped('partner_id').sudo().signup_prepare(signup_type="reset", expiration=expiration)

    def resend_invitation(self):
        if self.user_id:
            for users in self.user_id.sudo():
                users.action_reset_password()
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'type': 'success',
                'message': 'A password reset has been requested for this user. An email containing the following link has been sent.!',
                'sticky': True,
            }
        }
        return notification

    def sending_invitation(self):
        if not self.email:
            raise UserError(
                _("Email is required For Grant Portal Access Management...!")
            )
        user_env = self.env["res.users"].sudo()
        if self.state == 'draft':
            if user_env.search([("login", "=", self.email)], limit=1):
                raise UserError(
                    _(
                        "Another user is already registered using this Email."
                        " Please contact support for help.!"
                    )
                )
            partner_env = self.env["res.partner"].sudo()
            partner_id = partner_env.search([("email", "=", self.email)])
            partner_vals = {
                "name": self.name,
                "street": self.street,
                "street2": self.street2,
                "zip": self.zip,
                "city": self.city,
                "state_id": self.state_id.id or False,
                "country_id": self.country_id.id or False,
                "phone": self.phone,
                "website": self.website,
                "mobile": self.mobile,
                "email": self.email,
                "is_incident": True,
                "parent_id": self.manager_id.partner_id.id if self.manager_id and self.manager_id.partner_id else self.env.user.partner_id.id,
                "company_type": "person",
            }
            if self.is_company:
                if not self.company_partner_id:
                    company_id = partner_env.create({
                        "name": self.name
                    })
                    partner_vals.update({"parent_id": company_id.id})
                    self.company_partner_id = company_id.id
                else:
                    partner_vals.update({"parent_id": self.env.user.partner_id.parent_id.id})
                admin_role_id = self.env.ref("mysisco_incident_register.incident_role_admin").id
                self.incident_role_id = admin_role_id
            if not partner_id:
                partner_id = partner_env.create(partner_vals)
            else:
                partner_id.write(partner_vals)
            if partner_id:
                self.partner_id = partner_id.id
                portal_wiz_id = (
                    self.env["portal.wizard"]
                    .sudo()
                    .create({"partner_ids": [Command.set([partner_id.id])]})
                )
                portal_wiz_id.sudo().user_ids.action_grant_access()
            portal_group = self.env.ref('base.group_portal')
            user_group = self.env.ref('base.group_user')
            if self.incident_role_id == self.env.ref(
                    'mysisco_incident_register.incident_role_admin') or self.is_company:
                incident_register_admin = self.env.ref('mysisco_incident_register.group_incident_register_admin')
                portal_group.sudo().write({'users': [(3, partner_id.user_ids[0].id)]})
                user_group.sudo().write({'users': [(4, partner_id.user_ids[0].id)]})
                incident_register_admin.sudo().write({'users': [(4, partner_id.user_ids[0].id)]})
            elif self.incident_role_id == self.env.ref('mysisco_incident_register.incident_role_manager'):
                incident_manager_group = self.env.ref('mysisco_incident_register.group_incident_register_manager')
                portal_group.sudo().write({'users': [(3, partner_id.user_ids[0].id)]})
                user_group.sudo().write({'users': [(4, partner_id.user_ids[0].id)]})
                incident_manager_group.sudo().write({'users': [(4, partner_id.user_ids[0].id)]})
            else:
                incident_staff_group = self.env.ref('mysisco_incident_register.group_incident_register_staff')
                incident_staff_group.sudo().write({'users': [(4, partner_id.user_ids[0].id)]})
            self.state = 'posted'
            self.user_id = partner_id.user_ids[0].id

    def write(self, values):
        user_id = self.user_id.sudo()
        partner_list = [
            "name",
            "street",
            "street2",
            "zip",
            "city",
            "phone",
            "website",
            "country_id",
            "title",
            "state_id",
            "mobile",
            "email",
            "function"
        ]
        partner_vals = {key: values.get(key) for key in partner_list if values.get(key)}
        if partner_vals:
            user_id.partner_id.write(partner_vals)
        user_vals = {key: values.get(key) for key in ['active', 'email'] if values.get(key)}
        if user_vals:
            user_id.write(user_vals)
        return super(IncidentRegisterPartner, self).write(values)


class ResPartner(models.Model):
    _inherit = "res.partner"

    business_name = fields.Char()
    is_incident = fields.Boolean()
