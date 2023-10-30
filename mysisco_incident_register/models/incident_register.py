# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).


from odoo import Command, api, fields, models

STATUS_COLOR = {
    "unresolved": 23,  # red / danger
    "action_proposed": 17,  # green / success
    "investigation_complete": 2,  # orange
}


class IncidentRegister(models.Model):
    _name = "incident.register"
    _description = "Incident Register"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(string="Number")
    partner_id = fields.Many2one("res.partner", string="Partner")
    partner_name = fields.Char()
    date_received = fields.Date()
    description = fields.Text(string="Incident Description")
    subject = fields.Char(string="Impact/Injury to Subject")
    immediate_action = fields.Text(
        help="Immediate Action Taken to ensure the health and"
             " safety and wellbeing of person involved in the incident",
        string="Immediate Action Taken by staff",
    )
    send_notification_to = fields.Many2one(
        "send.notification.type", string="Notifications Required to Whom"
    )
    type_of_reportable = fields.Many2one(
        "notification.type.commission.incident",
        help="Type of reportable incident to NDIS Commission",
        string="Type of NDIS Commission",
    )
    guardian_notified = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
        string="Family, carer, guardian notified",
    )
    referred_to_authorised = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
        help="Referred to Authorised Reportable Incidents Notifier/Approver ",
        string="Referred to Authorised",
    )
    date_advised = fields.Datetime(string="Date and Time Advised")
    status = fields.Selection(
        [
            ("unresolved", "Unresolved"),
            ("action_proposed", "Action proposed"),
            ("investigation_complete", "Investigation complete"),

        ],
        default="action_proposed",
    )
    links = fields.Text(help="Links to relevant information")

    privacy_visibility = fields.Selection(
        [
            ("followers", "Invited internal users"),
            ("employees", "All internal users"),
            ("portal", "Invited portal users and all internal users"),
        ],
        string="Visibility",
        required=True,
        default="portal",
    )
    active = fields.Boolean(default=True)

    # Investigation Fields

    investigation_possible_causes = fields.Selection(
        [
            ("yes", "Yes"),
            ("no", "No"),
        ],
        help="Investigation Undertaken into possible causes",
        string="Investigation causes",
    )
    investigation_desc = fields.Text(
        help="Investigation Record of What Happened", string="Investigation Description"
    )
    investigation_findings = fields.Text()
    outcome_action = fields.Text(
        help="Outcome / Action following to mitigate further incidents",
        string="Outcome / Action",
    )
    investigation_actions = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Investigation Actions Completed"
    )
    action_complete_date = fields.Date(string="Investigation Action Date Completed")
    color = fields.Integer(string="Color Index", compute="_compute_last_update_color")
    last_update_color = fields.Integer(compute="_compute_last_update_color")
    user_id = fields.Many2one(
        "res.users",
        string="Register Manager",
        default=lambda self: self.env.user,
        tracking=True,
    )
    # Feedback Fields

    feedback_participat = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
        help="Participant feedback on incident handling process",
        string="Participant feedback",
    )
    comments = fields.Text(string="Feedback Comments")
    improvement_process_actions = fields.Text(
        help="Improvement to Process. Actions Required?",
        string="Improvement Actions Required?",
    )
    process_improvement = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
        help="Process improvement Implemented",
        string="improvement Process",
    )
    improvement_strategy_date = fields.Date(
        help="Improvement Strategies completed (Date)",
        string="Strategies completed Date",
    )
    report_quality_checked = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
    )
    feedback_attachment = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
    )
    closed_date = fields.Date(string="Date Incident Closed")
    collaborator_ids = fields.One2many(
        "incident.register.collaborator",
        "register_id",
        string="Collaborators",
        copy=False,
    )
    city = fields.Char()
    informed_time = fields.Float()
    time_of_incident = fields.Float()
    time_first_incident = fields.Float()
    date_first = fields.Date()
    contact_number = fields.Char()
    position = fields.Char()
    address = fields.Char()
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    # Participants: details

    full_name = fields.Char()
    date_of_birth = fields.Date()
    participant_address = fields.Char(string='Participant Address')
    involved_witness = fields.Char(string='Involved/Witness')
    injured = fields.Selection([("yes", "Yes"), ("no", "No")])
    medical_attention_required = fields.Selection([("yes", "Yes"), ("no", "No")])
    staff_full_name = fields.Char(string='Staff Name')
    staff_address = fields.Char(string='Staff Address')
    staff_other = fields.Selection(
        [("staff", "Staff"), ("carer", "Carer"), ("other", "Other")],
        string="Staff/Other",
    )
    incident_type = fields.Many2many(
        "incident.type",
        "incident_id",
        copy=False,
    )
    staff_involved_witness = fields.Char(string='Staff Involved/Witness')
    staff_injured = fields.Char(string="Injured?")
    staff_medical_attention_required = fields.Selection([("yes", "Yes"), ("no", "No")])
    before_incident = fields.Text(help="(eg. What was client doing before incident) ?")
    damaged_property = fields.Selection(
        [("yes", "Yes"), ("no", "No")], help="Was any property or equipment damaged?"
    )
    contacted_police = fields.Selection([("yes", "Yes"), ("no", "No")])
    details = fields.Text(string="Details of damage")
    incident_reported = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Incident reported to the Line Manager?"
    )
    date = fields.Date()
    attachment = fields.Char()
    signature = fields.Char()
    manager_name = fields.Char(string=' Manager’s name')
    phone = fields.Char()
    manager_position = fields.Char()
    what_action_taken = fields.Text(help="What action have been taken?")
    informed_date = fields.Date()
    investigation_action_date = fields.Date()
    token = fields.Char()
    website_form_step = fields.Integer()

    # is_super_admin = fields.Boolean(compute="_compute_is_super_admin")

    # @api.depends("status")
    # def _compute_is_super_admin(self):
    #     self.is_super_admin = False
    #     super_admin = self.user_has_groups('mysisco_incident_register.group_incident_register_super_admin')
    #     if super_admin:
    #         self.is_super_admin = True

    @api.depends("status")
    def _compute_last_update_color(self):
        for register in self:
            register.last_update_color = STATUS_COLOR[register.status]
            register.color = STATUS_COLOR[register.status]

    @api.model_create_multi
    def create(self, vals_list):
        # We generate a standard reference
        for vals in vals_list:
            vals["name"] = (
                    self.env["ir.sequence"].sudo().next_by_code("incident.register.seq")
                    or "/"
            )
        recs = super().create(vals_list)
        for rec in recs:
            rec._add_collaborators(partners=self.env.user.partner_id)
            rec.message_subscribe(partner_ids=self.env.user.partner_id.ids)

        return recs

    def _compute_access_url(self):
        res = super()._compute_access_url()
        for incident in res:
            incident.access_url = f"/my/incident/{incident.id}"
        return res

    def _check_incident_sharing_access(self):
        self.ensure_one()
        if self.privacy_visibility != "portal":
            return False
        if self.env.user.has_group("base.group_portal"):
            return (
                self.env["incident.register.collaborator"]
                .sudo()
                .search(
                    [
                        ("register_id", "=", self.sudo().id),
                        ("partner_id", "=", self.env.user.partner_id.id),
                    ]
                )
            )
        return self.env.user._is_internal()

    def _add_collaborators(self, partners):
        self.ensure_one()
        user_group_id = self.env["ir.model.data"]._xmlid_to_res_id("base.group_user")
        all_collaborators = self.collaborator_ids.partner_id
        new_collaborators = partners.filtered(
            lambda partner: partner not in all_collaborators
                            and (
                                    not partner.user_ids
                                    or user_group_id not in partner.user_ids[0].groups_id.ids
                            )
        )
        if not new_collaborators:
            # Then we have nothing to do
            return

        self.write(
            {
                "collaborator_ids": [
                    Command.create(
                        {
                            "partner_id": collaborator.id,
                        }
                    )
                    for collaborator in new_collaborators
                ],
            }
        )


class SendNotificationType(models.Model):
    _name = "send.notification.type"
    _description = "Send Notification Type"

    name = fields.Char()


class NotificationTypeCommission(models.Model):
    _name = "notification.type.commission.incident"
    _description = "Notification Type Commission"

    name = fields.Char()


class IncidentType(models.Model):
    _name = "incident.type"
    _description = "Incident Type"

    name = fields.Char()


class IncidentCity(models.Model):
    _name = "incident.city"
    _description = "Incident City"

    name = fields.Char(required=True)
    partner_id = fields.Many2one("res.partner", string="Company")
    total_emp = fields.Integer(string="Total Employee", compute="_compute_emp_count")

    @api.model
    def default_get(self, fields):
        res = super(IncidentCity, self).default_get(fields)
        admin = self.env.user.has_group('mysisco_incident_register.group_incident_register_admin')
        incident_partner_id = self.env['incident.register.partner'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
        if admin:
            res['partner_id'] = incident_partner_id.company_partner_id.id or incident_partner_id.partner_id.id
        return res

    def ims_action_open_employee(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'incident.register.partner',
            'name': 'Employee',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('incident_city_ids', '=', self.id), ('company_partner_id', '=', self.partner_id.id)],
            'context': {'default_is_company' : True, 'search_default_group_incident_role' : 1},
        }
    def _compute_emp_count(self):
        for rec in self:
            emp_num = self.env['incident.register.partner'].search_count([('incident_city_ids', '=', rec.id), ('company_partner_id', '=', rec.partner_id.id)])
            rec.total_emp = emp_num

class IncidentRole(models.Model):
    _name = "incident.role"
    _description = "Incident Role"

    name = fields.Char()

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        admin = self.env.ref('mysisco_incident_register.incident_role_admin')
        manager = self.env.ref('mysisco_incident_register.incident_role_manager')
        if self.env.user.has_group('mysisco_incident_register.group_incident_register_super_admin'):
            args = args
        elif self.env.user.has_group('mysisco_incident_register.group_incident_register_admin'):
            args.append(('id', 'not in', admin.ids))
        elif self.env.user.has_group('mysisco_incident_register.group_incident_register_manager'):
            args.append(('id', 'not in', admin.ids + manager.ids))
        res = super(IncidentRole, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                access_rights_uid=access_rights_uid)
        return res
