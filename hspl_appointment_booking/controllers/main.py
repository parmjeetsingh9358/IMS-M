from odoo.http import Controller, request, route
from datetime import date, datetime, timedelta
import pytz


class PublicCustomer(Controller):

    @route([
        "/appointment",
        "/appointment/<int:year>/<int:month>",

    ], type='http', auth='public', website=True)
    def appointment_create(self, year=None, month=None, **post):
        partner_id = request.env.user.partner_id
        booking_id = request.env['resource.booking'].sudo().search([('partner_id', '=', partner_id.id)], limit=1)
        type_id = request.env['resource.booking.type'].sudo().search([], limit=1)
        if not booking_id:
            request.env['resource.booking'].sudo().create({
                "partner_id": partner_id.id,
                "partner_ids": [(6, 0, partner_id.ids)],
                "type_id": type_id.id
            })
        values = booking_id.with_context(appointment_public=True)._get_calendar_context(year, month)
        return request.render("hspl_appointment_booking.appointment_select", values)

    @route(["/appointment/booking/<string:day>/<string:time>/<string:token>"], type='http', auth='public', website=True)
    def appointment_booking_data(self, day=False, time=False, token=False, **kwrgs):
        # booking = request.env['resource.booking'].search([],limit=1)
        partner_id = request.env.user.partner_id
        booking_id = request.env['resource.booking'].sudo().search([('partner_id', '=', partner_id.id)], limit=1)
        type_id = request.env['resource.booking.type'].sudo().search([], limit=1)
        if not booking_id:
            request.env['resource.booking'].sudo().create({
                "partner_id": partner_id.id,
                "partner_ids": [(6, 0, partner_id.ids)],
                "type_id": type_id.id
            })
        selected_date =  datetime.strptime(day, '%Y-%m-%d').date()
        selected_month = selected_date.month
        selected_year = selected_date.year

        values = booking_id.with_context(appointment_public=True)._get_calendar_context(selected_year, selected_month)
        available_slot = False
        time_format = values.get("res_lang").time_format.replace(':%S', '')
        for slot in values.get('slots').get(datetime.strptime(day, '%Y-%m-%d').date()):
            if slot.get('token') == token and slot.get('slot').strftime(time_format) == time:
                available_slot = True
                timezone_time = slot.get('slot')
        if not available_slot:
            return request.redirect('/appointment')
        values = {
            "day": day,
            "time_val": time,
            "token": token,
            'error': {}
        }
        if kwrgs.get('submit', False):
            res_partner_id = request.env['res.partner'].sudo().search([('email', '=', kwrgs.get('email'))], limit=1)
            if not res_partner_id:
                res_partner_id = request.env['res.partner'].with_context(lang=request.env.lang).sudo().create({
                    "name": kwrgs.get('name'),
                    "email": kwrgs.get('email'),
                    "phone": kwrgs.get('phone'),
                    'type': 'contact',
                    "tz": request.env.user.tz
                })
            resource_booking_id = request.env['resource.booking'].sudo().search(
                [('partner_id', '=', res_partner_id.id), ('state', '=', 'scheduled')], limit=1)
            if not resource_booking_id:
                resource_booking_id = booking_id.sudo().copy({
                    "name": res_partner_id.name + " with " + type_id.name,
                    "partner_id": res_partner_id.id,
                    "partner_ids": [(6, 0, res_partner_id.ids)],
                    "duration": type_id.duration,
                    "type_id": type_id.id,
                    "description":kwrgs.get('comment'),
                    "business_name": kwrgs.get('business_name'),
                    "categ_ids": [(6, 0, type_id.categ_ids.ids)],
                    "start": timezone_time.astimezone(tz=pytz.timezone('UTC')).replace(tzinfo=None)
                })
            else:
                resource_booking_id.start = timezone_time.astimezone(tz=pytz.timezone('UTC')).replace(tzinfo=None)
            return request.render("hspl_appointment_booking.appointment_success", {'booking_id': resource_booking_id})
        return request.render("hspl_appointment_booking.create_appointment", values)
