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
        // console.log("ApplicationNumberField setup called", this.props);

        this.state = useState({
            variant_names: this.props.record.data.selected_variant_names || [],
            values: {},
        });
        console.log("Initial values:", this.props.name, this.props.update());

    }

    onValueChange(variant_name, newValue) {
        this.state.values[variant_name] = newValue;
        console.log("Updated values:", this.state.values);

    }
}

export const application_number_field = {
    component: ApplicationNumberField,
};
registry.category("fields").add("application_number_field", application_number_field);
