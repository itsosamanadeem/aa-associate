/** odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { ListController } from "@web/views/list/list_controller";
import {
    Component,
    onMounted,
    onWillPatch,
    onWillRender,
    onWillStart,
    useEffect,
    useRef,
    useState,
    useSubEnv,
} from "@odoo/owl";

export class ActiveFields extends Component{
    static template="account_move_inherit.ActiveFields"
    setup(){
        console.log('this list is inherited');
    }
}
export const active_fields = {
    component: ActiveFields
};

registry.category("fields").add("active_fields", active_fields);