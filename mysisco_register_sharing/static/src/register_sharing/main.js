/** @odoo-module **/
import {startWebClient} from "@web/start";
import {RegisterSharingWebClient} from "./register_sharing";
import {prepareFavoriteMenuRegister} from "./components/favorite_menu_registry";

prepareFavoriteMenuRegister();
startWebClient(RegisterSharingWebClient);
