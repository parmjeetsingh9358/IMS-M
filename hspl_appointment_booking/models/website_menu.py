from odoo import models,fields\


class Menu(models.Model):
    _inherit = "website.menu"

    def _compute_visible(self):
        super(Menu ,self)._compute_visible()
        for menu in self:
            if menu.name == "Book Demo" and not self.env.user._is_public():
                menu.is_visible = False
            if menu.name == "Incident Register" and self.env.user._is_public():
                menu.is_visible = False