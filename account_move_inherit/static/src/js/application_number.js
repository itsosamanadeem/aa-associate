import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";


export class ApplicationNumberField extends Component {
    static template = "account_move_inherit.ApplicationNumberField";
    static props = {
        ...standardFieldProps,   // <-- this injects .value and .update
    };

    setup() {
        const variant_names = this.props.record.data.selected_variant_names || [];
        const existing = this.props.value || {};

        this.state = useState({
            variant_names,
            values: existing.values || {},
            selected: existing.selected || {},
        });
    }

    _commit() {
        // Now this.props.update exists ✅
        this.props.update({
            values: this.state.values,
            selected: this.state.selected,
        });
    }

    onVariantChange(variant_name, newVariant) {
        this.state.selected[variant_name] = newVariant;
        this._commit();
    }

    onValueChange(variant_name, newValue) {
        this.state.values[variant_name] = newValue;
        this._commit();
    }
}

export const application_number_field = {
    component: ApplicationNumberField,
    supportedTypes: ["json"],
};

registry.category("fields").add("application_number_field", application_number_field);
