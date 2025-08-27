/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useEffect } from "@odoo/owl";

export class ApplicationNumberField extends Component {
    static template = "account_move_inherit.ApplicationNumberField";

    setup() {
        console.log("ApplicationNumberField setup called", this.props);
        this.variant_names= this.props.record.data.selected_variant_names || [];
    }
}
export const application_number_field = {
    component: ApplicationNumberField,
};
registry.category("fields").add("simple_text", application_number_field);