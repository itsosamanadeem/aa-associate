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
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";

export class ActiveFields extends Component {
    static template = "account_move_inherit.ActiveFields"
    static components = { Many2XAutocomplete };
    setup() {
        this.getDomain = () => {
            return [["partner_id", "=", this.props.record.data.partner_id]];
        };
        this.onTrademarkSelected = (ev) => {
            const trademark = ev.detail; // selected record
            this.props.record.update({ trademark_id: trademark.id });
        };
    }
}
export const active_fields = {
    component: ActiveFields
};

registry.category("fields").add("active_fields", active_fields);