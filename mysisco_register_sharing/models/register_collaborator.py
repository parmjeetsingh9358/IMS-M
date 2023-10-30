# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class RegisterCollaborator(models.Model):
    _name = "register.collaborator"
    _description = "Collaborators in register shared"

    register_id = fields.Many2one(
        "complaint.register",
        "Register Shared",
        domain=[("privacy_visibility", "=", "portal")],
        required=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner", "Collaborator", required=True, readonly=True
    )
    partner_email = fields.Char(related="partner_id.email")

    _sql_constraints = [
        (
            "unique_collaborator",
            "UNIQUE(register_id, partner_id)",
            "A collaborator cannot be selected more than once in "
            "the register sharing access. Please remove duplicate(s) and try again.",
        ),
    ]

    def name_get(self):
        collaborator_search_read = self.search_read(
            [("id", "in", self.ids)], ["id", "register_id", "partner_id"]
        )
        return [
            (
                collaborator["id"],
                "%s - %s"
                % (collaborator["register_id"][1], collaborator["register_id"][1]),
            )
            for collaborator in collaborator_search_read
        ]

    @api.model_create_multi
    def create(self, vals_list):
        collaborator = self.env["register.collaborator"].search([], limit=1)
        register_collaborators = super().create(vals_list)
        if not collaborator:
            self._toggle_register_sharing_portal_rules(True)
        return register_collaborators

    def unlink(self):
        res = super().unlink()
        # Check if it remains at least a collaborator in all shared registers.
        collaborator = self.env["register.collaborator"].search([], limit=1)
        if not collaborator:  # then disable the register sharing feature
            self._toggle_register_sharing_portal_rules(False)
        return res

    @api.model
    def _toggle_register_sharing_portal_rules(self, active):
        """Enable/disable register sharing feature
        When the first collaborator is added in
        the model then we need to enable the feature.
        In the inverse case, if no collaborator is
        stored in the model then we disable the feature.
        To enable/disable the feature, we just need to
        enable/disable the ir.model.access and ir.rule
        added to portal user that we do not want
        to give when we know the register sharing is unused.
        :param active: contains boolean value, True to enable
        the register sharing feature, otherwise we disable the feature.
        """
        access_register_sharing_portal = self.env.ref(
            "mysisco_complain_register.access_register_sharing_task_portal"
        ).sudo()
        if access_register_sharing_portal.active != active:
            access_register_sharing_portal.write({"active": active})

        task_portal_ir_rule = self.env.ref(
            "mysisco_complain_register.register_task_rule_portal_register_sharing"
        ).sudo()
        if task_portal_ir_rule.active != active:
            task_portal_ir_rule.write({"active": active})
