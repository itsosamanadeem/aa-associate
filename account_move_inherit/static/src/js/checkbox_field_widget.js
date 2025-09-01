/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class InvoiceLineListRendererWithFieldCheckbox extends ListRenderer {
    static components = { ...ListRenderer.components, CheckBox };
    static recordRowTemplate = "account_move_inherit.ListRenderer.RecordRowWithCheckbox";
    setup() {
        super.setup()

    }
    onFieldCheckboxToggle(record, fieldName, ev) {
        const checked = ev.target.checked;
        const recId = record.resId || record.id;   // use real db ID if exists, else virtual ID
        console.log('Toggle for', recId, fieldName, checked);

        // Clone current flags
        const newFlags = Object.assign({}, record.data.extra_flags || {});

        // Ensure line entry exists
        if (!newFlags[recId]) {
            newFlags[recId] = [];
        }

        // Add or remove field from array
        if (checked) {
            if (!newFlags[recId].includes(fieldName)) {
                newFlags[recId].push(fieldName);
            }
        } else {
            newFlags[recId] = newFlags[recId].filter(f => f !== fieldName);
        }

        record.update({ extra_flags: newFlags });
    }


}

export class InvoiceLineOne2ManyWithFieldCheckbox extends X2ManyField {
    static components = {
        ...X2ManyField.components,
        ListRenderer: InvoiceLineListRendererWithFieldCheckbox,
    };
}

registry.category("fields").add("invoiceLine_list_renderer_with_checkbox", {
    ...x2ManyField,
    component: InvoiceLineOne2ManyWithFieldCheckbox,
});
