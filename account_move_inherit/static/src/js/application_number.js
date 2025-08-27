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
        // console.log("ApplicationNumberField setup called", this.props);
        let initialValue = this.props.record.data[this.props.name];
        if (typeof initialValue === "string") {
            try {
                initialValue = JSON.parse(initialValue);
            } catch (e) {
                initialValue = {};
            }
        }
        this.state = useState({
            variant_names: this.props.record.data.selected_variant_names || [],
            values: initialValue || {}
        });

        onWillStart(()=>{
            console.log("onWillStart - Initial values:", this.props)
        })
        onWillUpdateProps((prop)=>{
            console.log(prop, "prop");
            
            // this.onValueChange(prop.name, this.getValue())
        })
        console.log("Initial values:", this.props.value);

    }

    getValue() {
        return JSON.parse(this.props.record.data[this.props.name]);
    }
    onValueChange(variant_name, newValue) {
        this.state.values[variant_name] = parseInt(newValue) || 0;
        console.log("Updated values:", this.state.values);
        this.props.record.update(JSON.parse(this.state.values))
    }
}

export const application_number_field = {
    component: ApplicationNumberField,
    supportedTypes: ["json"],
};
registry.category("fields").add("application_number_field", application_number_field);
