# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class IncidentRegisterShareWizard(models.TransientModel):
    _name = "incident.register.share.wizard"
    _inherit = "portal.share"
    _description = "Incident Register Sharing"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if not result.get("access_mode"):
            result.update(
                access_mode="read",
                display_access_mode=True,
            )
        return result

    @api.model
    def _selection_target_model(self):
        register_model = self.env["ir.model"]._get("incident.register")
        return [(register_model.model, register_model.name)]

    access_mode = fields.Selection([("read", "Readonly"), ("edit", "Edit")])
    display_access_mode = fields.Boolean()

    @api.depends("res_model", "res_id")
    def _compute_resource_ref(self):
        for incident in self:
            if incident.res_model and incident.res_model == "incident.register":
                incident.resource_ref = "%s,%s" % (
                    incident.res_model,
                    incident.res_id or 0,
                )
            else:
                incident.resource_ref = None

    def action_send_mail(self):
        self.ensure_one()
        if self.access_mode == "edit":
            portal_partners = self.partner_ids.filtered("user_ids")
            note = self._get_note()
            self.resource_ref._add_collaborators(self.partner_ids)
            self._send_public_link(note, portal_partners)
            self._send_signup_link(note, partners=self.partner_ids - portal_partners)
            self.resource_ref.message_subscribe(partner_ids=self.partner_ids.ids)
            return {"type": "ir.actions.act_window_close"}
        return super().action_send_mail()
