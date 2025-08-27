/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ApplicationNumberField extends Component {
    static template = "account_move_inherit.ApplicationNumberField";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.state = useState({
            variant_names: this.props.record.data.selected_variant_names || [],
            values: this.props.value || {},   // load from field value
        });
    }

    onValueChange(variant_name, newValue) {
        // Update local state
        this.state.values[variant_name] = parseInt(newValue) || 0;

        // Persist to ORM using update()
        this.props.update(this.state.values);
    }
}

export const application_number_field = {
    component: ApplicationNumberField,
    supportedTypes: ["json"],
};
registry.category("fields").add("application_number_field", application_number_field);
