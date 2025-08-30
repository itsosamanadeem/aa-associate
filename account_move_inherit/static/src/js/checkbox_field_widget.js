/** odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Component, useState, onWillUpdateProps, onWillStart } from "@odoo/owl";

export class CheckboxCheck extends Component {
    static template = "account_move_inherit.CheckboxCheck"
    static props = {
        ...standardFieldProps,
    }
    static components = {
        CheckBox,
    };
    setup() {}

    onToggle(ev) {
        const record = this.props.record;
        const fieldName = this.props.name;
        const checked = ev.target.checked;

        const newFlags = Object.assign({}, record.data.extra_flags || {});
        newFlags[fieldName] = checked;

        record.update({ extra_flags: newFlags });
    }

}
export const checkbox_check = {
    component: CheckboxCheck
};

registry.category("fields").add("checkbox_check", checkbox_check);