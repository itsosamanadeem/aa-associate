/** odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { ListController } from "@web/views/list/list_controller";

export class ActiveFields extends ListController{
    setup(){
        super.setup()
        console.log('this list is inherited');
    }
}
export const active_fields = {
    ...listView,
    ...ListRenderer,
    Controller: ActiveFields,
};

registry.category("views").add("active_fields", active_fields);