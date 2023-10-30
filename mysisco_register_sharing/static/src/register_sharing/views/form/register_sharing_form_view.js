/** @odoo-module */

import {formView} from "@web/views/form/form_view";
import {RegisterSharingFormController} from "./register_sharing_form_controller";
import {RegisterSharingFormRenderer} from "./register_sharing_form_renderer";

formView.Controller = RegisterSharingFormController;
formView.Renderer = RegisterSharingFormRenderer;
