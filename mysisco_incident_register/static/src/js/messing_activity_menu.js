/** @odoo-module **/

import { MessagingMenuContainer } from "@mail/components/messaging_menu_container/messaging_menu_container";
import { ActivityMenuView } from "@mail/components/activity_menu_view/activity_menu_view";
import { patch } from "@web/core/utils/patch";

const { onWillStart } = owl;

patch(MessagingMenuContainer.prototype, 'CustomMessagingMenuContainer', {

    setup() {
        const CustomMessagingMenuSuper = this._super(...arguments);
        onWillStart(async () => {
            this.IsGroupHasAccess = await this.env.services.orm.user.hasGroup('mysisco_incident_register.group_incident_register_staff');
//            debugger;
        });
        return CustomMessagingMenuSuper
    }
})

patch(ActivityMenuView.prototype, 'CustomActivityMenuView', {

    setup() {
        const CustomActivityMenuSuper = this._super(...arguments);
        onWillStart(async () => {
            this.IsGroupHasAccess = await this.env.services.orm.user.hasGroup('mysisco_incident_register.group_incident_register_staff');
//            debugger;
        });
        return CustomActivityMenuSuper
    }
})