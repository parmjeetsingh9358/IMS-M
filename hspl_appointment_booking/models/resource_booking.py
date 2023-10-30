from odoo import models,fields


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    business_name = fields.Char()

    def _get_available_slots(self, start_dt, end_dt):
        res = super(ResourceBooking, self)._get_available_slots(start_dt=start_dt, end_dt=end_dt)
        if self.env.context.get('appointment_public', False):
            result = {}
            i = 1
            for date, list_val in res.items():
                for slot_val in list_val:
                    i += (1 * 5) / 100
                    if not result.get(date, False):
                        result.setdefault(date, [])
                    result[date].append(
                        {"token": slot_val.strftime("%Y-%m-%d-%H-00-00") + str(i), "slot": slot_val})
            return result
        else:
            return res
