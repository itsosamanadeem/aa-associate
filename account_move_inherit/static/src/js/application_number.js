/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

export class ApplicationNumberField extends Component {
    static template = "account_move_inherit.ApplicationNumberField";

    setup() {
        console.log("ApplicationNumberField setup called", this.props);

        const variant_names = this.props.record.data.selected_variant_names || [];

        // Initialize rows equal to number of variants
        this.state = useState({
            variant_names,
            rows: variant_names.map((name, index) => ({
                index,
                variant: name, // default select
                value: "",     // empty number
            })),
        });
    }

    onVariantChange(index, newVariant) {
        const row = this.state.rows.find(r => r.index === index);
        if (row) {
            row.variant = newVariant;
        }
        console.log("Updated rows:", this.state.rows);
    }

    onValueChange(index, newValue) {
        const row = this.state.rows.find(r => r.index === index);
        if (row) {
            row.value = newValue;
        }
        console.log("Updated rows:", this.state.rows);
    }
}

export const application_number_field = {
    component: ApplicationNumberField,
};
registry.category("fields").add("application_number_field", application_number_field);
