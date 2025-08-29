/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ActiveFields extends Component {
    static template = "account_move_inherit.ActiveFields";

    // ✅ Declare allowed props
    static props = {
        ...standardFieldProps,
    };

    static components = {
        Many2XAutocomplete,
        CheckBox,
    };

    setup() {
        console.log("Trademark field:", this.props.record.fields.trademark_id);

        this.getDomain = () => {
            return [["partner_id", "=", this.props.record.data.partner_id]];
        };

        this.onUpdateTrademark = async (value) => {
            let newVal = false;
            if (value && value.length) {
                const rec = value[0];
                newVal = [rec.id, rec.display_name];
            }
            await this.props.record.update({ trademark_id: newVal });
        };

        this.onToggleActive = async () => {
            await this.props.record.update({
                active: !this.props.record.data.active,
            });
        };
    }
}

registry.category("fields").add("active_fields", ActiveFields);
