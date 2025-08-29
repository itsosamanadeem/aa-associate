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
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ActiveFields extends Component {
    static template = "account_move_inherit.ActiveFields"
    static components = {
        Many2XAutocomplete,
        ...standardFieldProps,
    };
    setup() {
        this.getDomain = () => {
            return [["partner_id", "=", this.props.record.data.partner_id]];
        };
        console.log('this.env', this.env.searchModel);
        this.onUpdateTrademark = async (value) => {
            // 1. Update Odoo record value
            await this.props.record.update(
            {[this.props.name]: value}
            );

            // 2. Run custom logic
            console.log("Trademark updated to:", value);

            // e.g., call a method on the record, reload, etc.
            // this.env.bus.trigger("some_event", { recordId: this.props.record.resId });
        };
    }
}
export const active_fields = {
    component: ActiveFields
};

registry.category("fields").add("active_fields", active_fields);