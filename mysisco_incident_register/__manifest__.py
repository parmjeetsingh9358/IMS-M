# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

{
    "name": "Incident Register Manual",
    "version": "16.0.1.0.0",
    "author": "Heliconia Solutions Pvt. Ltd.",
    "website": "https://heliconia.io/",
    "depends": [
        "base",
        "mail",
        "analytic",
        "base_setup",
        "portal",
        "resource",
        "web",
        "website",
        "sale",
        "mysisco_register_sharing",
        "report_xlsx",
        "hspl_appointment_booking",
        "subscription_package"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/incident_notification_type_data.xml",
        "data/incident_role_data.xml",
        "data/incident_register_data.xml",
        "data/incident_register_sequence.xml",
        "data/website_model_access_data.xml",
        "wizard/incident_register_share_wizard_views.xml",
        "views/incident_register_view.xml",
        "views/portal_template.xml",
        "views/incident_role_view.xml",
        "views/incident_city_view.xml",
        "views/incident_type_view.xml",
        "views/incident_sharing_views.xml",
        "views/progress_wizard_template.xml",
        "views/website_form_templates.xml",
        "views/website_template.xml",
        # "views/navbar_header.xml",
        "views/incident_employees.xml",
        "views/incident_company.xml",
        "report/incident_register_report.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "mysisco_incident_register/static/src/scss/custom_frontend.scss",
            "mysisco_incident_register/static/src/scss/website_sale_frontend.scss",
        ],
        "web.assets_backend": [
            "mysisco_incident_register/static/src/js/messing_activity_menu.js",
            "mysisco_incident_register/static/src/xml/messing_activity_menu.xml",
            "mysisco_incident_register/static/src/list_renderer.xml",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}
