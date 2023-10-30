from collections import OrderedDict

from odoo import _, conf, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv.expression import AND, OR

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CustomPortalController(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "incident_count" in counters:
            incident_register_model = request.env["incident.register"]
            incident_count = (
                incident_register_model.search_count([])
                if incident_register_model.check_access_rights(
                    "read", raise_exception=False
                )
                else 1
            )
            values["incident_count"] = incident_count
        return values

    @http.route("/my/incident", type="http", auth="user", website=True)
    def my_incident_page(
        self,
        page=1,
        sortby=None,
        filterby=None,
        search=None,
        search_in=None,
        groupby=None,
        **kw
    ):
        incident_register = request.env["incident.register"]
        if not incident_register.check_access_rights("read", raise_exception=False):
            return request.redirect("/my")

        values = self._prepare_portal_layout_values()
        searchbar_sortings = dict(
            sorted(
                self._incident_get_searchbar_sortings().items(),
                key=lambda item: item[1]["sequence"],
            )
        )

        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }

        searchbar_inputs = self._incident_get_searchbar_inputs()

        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        if not filterby:
            filterby = "all"
        domain = searchbar_filters.get(filterby, searchbar_filters.get("all"))["domain"]
        if kw.get("category_id"):
            domain.append(("category_id", "=", int(kw.get("category_id"))))

        if not groupby:
            groupby = "none"

        if not search_in:
            search_in = "all"
        if search:
            domain += self._incident_search_domain(search_in, search)

        domain = AND(
            [
                domain,
                request.env["ir.rule"]._compute_domain(incident_register._name, "read"),
            ]
        )

        # count for pager
        incident_count = incident_register.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/incident",
            url_args={
                "sortby": sortby,
                "filterby": filterby,
                "groupby": groupby,
                "search": search,
                "search_in": search_in,
            },
            total=incident_count,
            page=page,
            step=self._items_per_page,
        )

        incident_ids = incident_register.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )

        values.update(
            {
                "grouped_incident": incident_ids,
                "page_name": "incident",
                "default_url": "/my/incident",
                "pager": pager,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "search": search,
                "sortby": sortby,
                "groupby": groupby,
                "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
                "filterby": filterby,
            }
        )
        return request.render(
            "mysisco_incident_register.incident_register_templates", values
        )

    def _incident_get_searchbar_inputs(self):
        values = {
            "all": {"input": "all", "label": _("Search in All"), "order": 1},
            "number": {
                "input": "name",
                "label": _("Search in Service Number"),
                "order": 2,
            },
            "name": {
                "input": "company_name",
                "label": _("Search in Name"),
                "order": 3,
            },
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _incident_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ("name", "all"):
            search_domain.append([("name", "ilike", search)])
        return OR(search_domain)

    def _incident_get_searchbar_sortings(self):
        return {
            "date": {
                "label": _("Newest"),
                "order": "create_date desc",
                "sequence": 1,
            },
            "name": {"label": _("Title"), "order": "name", "sequence": 2},
        }

    def _prepare_incident_sharing_session_info(self, incident):
        session_info = request.env["ir.http"].session_info()
        user_context = dict(request.env.context) if request.session.uid else {}
        mods = conf.server_wide_modules or []
        if request.env.lang:
            lang = request.env.lang
            session_info["user_context"]["lang"] = lang
            # Update Cache
            user_context["lang"] = lang
        lang = user_context.get("lang")
        translation_hash = request.env["ir.http"].get_web_translations_hash(mods, lang)
        cache_hashes = {
            "translations": translation_hash,
        }
        incident_company = incident.company_id
        session_info.update(
            cache_hashes=cache_hashes,
            action_name="mysisco_incident_register.incident_register_sharing_action",
            incident_id=incident.id,
            user_companies={
                "current_company": incident_company.id,
                "allowed_companies": {
                    incident_company.id: {
                        "id": incident_company.id,
                        "name": incident_company.name,
                    },
                },
            },
            # FIXME: See if we prefer to give only the currency that the portal
            #  user just need to see the correct information in register sharing
            currencies=request.env["ir.http"].get_currencies(),
        )
        return session_info

    @http.route(
        [
            "/my/incident/<int:incident_id>",
            "/my/incident/<int:incident_id>/page/<int:page>",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def my_incident_register_portal(
        self,
        incident_id=None,
        access_token=None,
    ):
        try:
            incident_sudo = self._document_check_access(
                "incident.register", incident_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        incident_id = request.env["incident.register"].sudo().browse(incident_id)
        values = {"incident_id": incident_id}
        user = request.env.user.partner_id
        if (
            incident_sudo.with_user(request.env.user)._check_incident_sharing_access()
            and user.active_subscription
        ):
            values = {"incident_id": incident_id.id}
            return request.render(
                "mysisco_incident_register.incident_sharing_portal", values
            )
        return request.render(
            "mysisco_incident_register.portal_my_incident_register", values
        )

    @http.route(
        "/my/incident/<int:incident_id>/incident_sharing_portal",
        type="http",
        auth="user",
        methods=["GET"],
    )
    def render_incident_backend_view(self, incident_id):
        incident_obj = request.env["incident.register"].sudo().browse(incident_id)
        if (
            not incident_obj.exists()
            or not incident_obj.with_user(
                request.env.user
            )._check_incident_sharing_access()
        ):
            return request.not_found()
        return request.render(
            "mysisco_incident_register.incident_sharing_embed",
            {"session_info": self._prepare_incident_sharing_session_info(incident_obj)},
        )
