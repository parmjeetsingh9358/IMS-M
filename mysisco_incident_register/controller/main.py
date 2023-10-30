from odoo import Command, http, _
from odoo.http import request
from psycopg2 import IntegrityError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

import werkzeug.utils
import json
import uuid

time_fields = ["time_of_incident", "informed_time", "time_first_incident"]
date_fields = ["date_received", "action_complete_date",
               "improvement_strategy_date", "closed_date", "date_first",
               "date_of_birth", "date", "informed_date", "investigation_action_date", ""]


class IncidentRegisterForm(http.Controller):
    @http.route([
        "/incident/register",
        "/incident/register/<string:token>"
    ], auth="user", website=True)
    def incident_register_form(self, token=False, **kwargs):
        errors = {}
        incident_id = False
        if token:
            incident_id = (
                request.env["incident.register"]
                .sudo()
                .search([('token', '=', token)])
            )
        values = {}
        if incident_id:
            values.update({
                "partner_name": kwargs.get("partner_name", incident_id.partner_name or ""),
                "contact_number": kwargs.get("contact_number", incident_id.contact_number or ""),
                "position": kwargs.get("position", incident_id.position or ""),
                "city": kwargs.get("city", incident_id.city or ""),
            })
        return request.render(
            "mysisco_incident_register.incident_reporter_template",
            {
                "error": errors,
                "checkout": values,
                "token": token,
                "incident_id": incident_id,
            },
        )

    @http.route([
        "/incident/success"
    ], auth="public", website=True)
    def incident_register_form_success(self, **kwargs):
        register_str = kwargs.get("str")
        record = request.env[request.session.form_builder_model_model].sudo().browse(request.session.form_builder_id)
        if not record or not register_str:
            return request.redirect("/incident/register")
        return request.redirect("/incident/%s/%s" % (register_str, record.token))

    @http.route([
        "/incident/details/<string:token>"
    ], auth="public", website=True)
    def incident_details_form(self, token=False, **kwargs):
        errors = {}
        if not token:
            return request.redirect("/incident/register")
        incident_id = (
            request.env["incident.register"]
            .sudo()
            .search([('token', '=', token)])
        )
        incident_type = request.env["incident.type"].search([])
        values = {
            "date_received": kwargs.get("date_received", incident_id.date_received and incident_id.date_received.strftime('%d/%m/%Y') or ""),
            "time_of_incident": str(kwargs.get("time_of_incident", incident_id.time_of_incident or "")).replace('.' , ':'),
            "date_first": kwargs.get("date_first", incident_id.date_first and incident_id.date_first.strftime('%d/%m/%Y') or ""),
            "time_first_incident": str(kwargs.get("time_first_incident", incident_id.time_first_incident or "")).replace('.' , ':'),
            "address": kwargs.get("address", incident_id.address or ""),
        }
        return request.render(
            "mysisco_incident_register.incident_details_template",
            {
                "error": errors,
                "token": token,
                "incident_type": incident_type,
                "checkout": values,
                "incident_id": incident_id,
            },
        )

    @http.route([
        "/incident/involved/<string:token>"
    ], auth="public", website=True)
    def incident_involved_form(self, token=False, **kwargs):
        errors = {}
        if not token:
            return request.redirect("/incident/register")
        incident_id = (
            request.env["incident.register"]
            .sudo()
            .search([('token', '=', token)])
        )

        values = {
            "full_name": kwargs.get("full_name", incident_id.full_name or ""),
            "date_of_birth": kwargs.get("date_of_birth", incident_id.date_of_birth and incident_id.date_of_birth.strftime('%d/%m/%Y') or ""),
            "participant_address": kwargs.get("participant_address", incident_id.participant_address or ""),
            "involved_witness": kwargs.get("involved_witness", incident_id.involved_witness or ""),
            "injured": kwargs.get("injured", incident_id.injured or ""),
            "medical_attention_required": kwargs.get("medical_attention_required",
                                                     incident_id.medical_attention_required or ""),
            "staff_full_name": kwargs.get("staff_full_name", incident_id.staff_full_name or ""),
            "staff_address": kwargs.get("staff_address", incident_id.staff_address or ""),
            "staff_other": kwargs.get("staff_other", incident_id.staff_other or ""),
            "staff_involved_witness": kwargs.get("staff_involved_witness", incident_id.staff_involved_witness or ""),
            "staff_injured": kwargs.get("staff_injured", incident_id.staff_injured or ""),
        }
        return request.render(
            "mysisco_incident_register.incident_involved_template",
            {
                "error": errors,
                "token": token,
                "checkout": values,
                "incident_id": incident_id,
            },
        )

    @http.route([
        "/incident/background/<string:token>"
    ], auth="public", website=True)
    def incident_background_form(self, token=False, **kwargs):
        errors = {}
        if not token:
            return request.redirect("/incident/register")
        incident_id = (
            request.env["incident.register"]
            .sudo()
            .search([('token', '=', token)])
        )
        values = {
            "before_incident": kwargs.get("before_incident", incident_id.before_incident or "")
        }
        return request.render(
            "mysisco_incident_register.incident_background_template",
            {
                "error": errors,
                "token": token,
                "checkout": values,
                "incident_id": incident_id,
            },
        )

    @http.route([
        "/incident/happened/<string:token>"
    ], auth="public", website=True)
    def incident_happened_form(self, token=False, **kwargs):
        errors = {}
        if not token:
            return request.redirect("/incident/register")
        incident_id = (
            request.env["incident.register"]
            .sudo()
            .search([('token', '=', token)])
        )
        # values = kwargs or {}
        values = {
            "manager_name": kwargs.get("manager_name", incident_id.manager_name),
            "incident_reported": kwargs.get("incident_reported", incident_id.incident_reported),
            "damaged_property": kwargs.get("damaged_property", incident_id.damaged_property),
            "contacted_police": kwargs.get("contacted_police", incident_id.contacted_police),
            "date": kwargs.get("date",incident_id.date and incident_id.date.strftime('%d/%m/%Y') or ""),
            "attachment": kwargs.get("attachment", incident_id.attachment),
            "description": kwargs.get("description", incident_id.description),
            "immediate_action": kwargs.get("immediate_action", incident_id.immediate_action),
            "signature": kwargs.get("signature", incident_id.signature),
            "details": kwargs.get("details", incident_id.details),
        }
        return request.render(
            "mysisco_incident_register.incident_happened_template",
            {
                "error": errors,
                "checkout": values,
                "token": token,
                "incident_id": incident_id,
            },
        )

    @http.route("/incident/thank-you/<string:token>", auth="public", website=True)
    def incident_thankyou_page(self, token=False, **kw):
        incident_id = (
            request.env["incident.register"]
            .sudo()
            .search([('token', '=', token)])
        )
        if not incident_id:
            return werkzeug.utils.redirect("/")
        else:
            return request.render(
                "mysisco_incident_register.incident_thanks_template",
                {"indent_request_id": incident_id},
            )


class WebsiteFormInherited(WebsiteForm):
    def write_record(self, model, values, id_record):
        model_name = model.sudo().model
        if model_name == 'incident.register':
            id_record.write(values)
        return id_record

    def insert_record(self, request, model, values, custom, meta=None):
        model_name = model.sudo().model
        if model_name == 'incident.register':
            values.update({'token': uuid.uuid4()})
            record = request.env[model_name].sudo().with_context(
                commit_assetsbundle=False,
            ).create(values)
            return record.id
        return super(WebsiteFormInherited).insert_record(request=request, model=model, values=values, custom=custom,
                                                         meta=meta)

    def _handle_incident_website_form(self, model_name, **kwargs):
        model_record = request.env['ir.model'].sudo().search(
            [('model', '=', model_name), ('website_form_access', '=', True)])
        for fields in date_fields:
            if kwargs.get(fields):
                input_date = datetime.strptime(kwargs.get(fields), '%d/%m/%Y')
                kwargs[fields] = input_date.strftime('%Y-%m-%d')
        for fields in time_fields:
            if kwargs.get(fields):
                kwargs[fields] = float(kwargs.get(fields).replace(":", "."))
        type_list = []
        for type_id in request.env["incident.type"].search([]):
            selected_val = kwargs.pop('%s_%s' % ('prefix', type_id.id), False)
            if selected_val:
                type_list.append(int(selected_val))
        if not model_record:
            return json.dumps({
                'error': _("The form's specified model does not exist")
            })
        try:
            data = self.extract_data(model_record, kwargs)
        # If we encounter an issue while extracting data
        except ValidationError as e:
            # I couldn't find a cleaner way to pass data to an exception
            return json.dumps({'error_fields': e.args[0]})

        try:
            if kwargs.get("token"):
                if type_list and data.get('record'):
                    data['record']['incident_type'] = [Command.set(type_list)]
                id_record = request.env[model_name].sudo().search([('token', '=', kwargs.get("token"))], limit=1)
                self.write_record(model_record, data['record'], id_record)
                id_record = id_record.id
            else:
                id_record = self.insert_record(request, model_record, data['record'], data['custom'], data.get('meta'))
            if id_record:
                self.insert_attachment(model_record, id_record, data['attachments'])
                # in case of an email, we want to send it immediately instead of waiting
                # for the email queue to process
                if model_name == 'mail.mail':
                    request.env[model_name].sudo().browse(id_record).send()

        # Some fields have additional SQL constraints that we can't check generically
        # Ex: crm.lead.probability which is a float between 0 and 1
        # TODO: How to get the name of the erroneous field ?
        except IntegrityError:
            return json.dumps(False)

        request.session['form_builder_model_model'] = model_record.model
        request.session['form_builder_model'] = model_record.name
        request.session['form_builder_id'] = id_record
        return json.dumps({'id': id_record})

    @http.route('/website/form/incident.register.report', type='http', auth="public", methods=['POST'], website=True)
    def website_form_incident(self, **kwargs):
        try:
            with request.env.cr.savepoint():
                if request.env['ir.http']._verify_request_recaptcha_token('website_form'):
                    # request.params was modified, update kwargs to reflect the changes
                    kwargs = dict(request.params)
                    return self._handle_incident_website_form("incident.register", **kwargs)
            error = _("Suspicious activity detected by Google reCaptcha.")
        except (ValidationError, UserError) as e:
            error = e.args[0]
        return json.dumps({
            'error': error,
        })


class SignupVerifyPartner(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        res = super(SignupVerifyPartner, self).web_auth_signup(*args, **kw)
        user = request.env['res.users'].sudo().search([("login", "=", qcontext.get("login"))])
        if user and user.partner_id.active_subscription:
            group = request.env.ref('base.group_user')
            portal_group = request.env.ref('base.group_portal')
            incident_admin_group = request.env.ref('mysisco_incident_register.group_incident_register_admin')
            portal_group.sudo().write({'users': [(3, user.id)]})
            group.sudo().write({'users': [(4, user.id)]})
            incident_admin_group.sudo().write({'users': [(4, user.id)]})
        return res
