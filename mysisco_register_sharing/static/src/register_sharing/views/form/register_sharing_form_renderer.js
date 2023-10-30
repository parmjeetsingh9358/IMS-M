/** @odoo-module */

import {ChatterContainer} from "../../components/chatter/chatter_container";
import {FormRenderer} from "@web/views/form/form_renderer";

export class RegisterSharingFormRenderer extends FormRenderer {}
RegisterSharingFormRenderer.components = {
    ...FormRenderer.components,
    ChatterContainer,
};
