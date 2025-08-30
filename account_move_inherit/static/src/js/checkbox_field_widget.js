/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, onWillStart } from "@odoo/owl";

export class FieldWithCheckbox extends Component {
    static template = "account_move_inherit.FieldWithCheckbox";
    static props = {
        ...standardFieldProps,
        InnerField: { type: Object },   // original field widget
    };
    static components = { CheckBox };

    onToggle(ev) {
        const record = this.props.record;
        const fieldName = this.props.name;
        const checked = ev.target.checked;

        const newFlags = Object.assign({}, record.data.field_flags || {});
        newFlags[fieldName] = checked;

        record.update({ field_flags: newFlags });
    }
}

registry.category("fields").add("with_checkbox", {
    component: FieldWithCheckbox,
    extractProps: (fieldInfo, dynamicInfo) => {
        // wrap original field widget
        const original = registry.category("fields").get(fieldInfo.widget || fieldInfo.type);
        return {
            InnerField: original.component,
            ...dynamicInfo,
        };
    },
});
