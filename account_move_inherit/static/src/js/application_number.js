/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

export class ApplicationNumberField extends Component {
    static template = "account_move_inherit.ApplicationNumberField";

    setup() {
        const variant_names = this.props.record.data.selected_variant_names || [];
        const existing = this.props.value || {};

        this.state = useState({
            variant_names,
            values: existing.values || {},       // { "Red": 10, "Blue": 5 }
            selected: existing.selected || {},   // { "Red": "Red", "Blue": "Blue" }
        });
    }

    _commit() {
        // Write back to DB
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
    supportedTypes: ["json"],   // store in fields.Json
};
registry.category("fields").add("application_number_field", application_number_field);
