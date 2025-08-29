/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillUpdateProps, onWillStart } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ApplicationNumberField extends Component {
    static template = "account_move_inherit.ApplicationNumberField";
    static props = {
        ...standardFieldProps,
    };
    setup() {
        
        let initialValue = this.props.record.data[this.props.name];

        if (typeof initialValue === "string") {
            try {
                initialValue = JSON.parse(initialValue);
            } catch {
                initialValue = {};
            }
        }

        this.state = useState({
            variant_names: this.props.record.data.selected_variant_names || [],
            values: initialValue || {},
        });

    }
    onValueChange(variant_name, newValue) {
        if (parseInt(newValue) < 0){
            return;
        }
        this.state.values[variant_name] = parseInt(newValue) || 0;
        this.props.record.update({
            [this.props.name]: this.state.values,
        });

        console.log("Updated values:", this.state.values);
    }

}

export const application_number_field = {
    component: ApplicationNumberField,
    supportedTypes: ["json"],
};
registry.category("fields").add("application_number_field", application_number_field);
