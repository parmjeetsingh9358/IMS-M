# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        subscription_env = self.env["subscription.package"].sudo()
        status = (self.env["subscription.package.stage"].sudo().search([("category", "=", "progress")], limit=1))
        res = super(SaleOrder, self).action_confirm()
        package = subscription_env.search([('sale_order', '=', self.id)])
        package.stage_id = status
        return res
