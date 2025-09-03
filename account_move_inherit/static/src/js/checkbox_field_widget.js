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
        const recId = record.resId || record.id;
        console.log('Toggle for', recId, fieldName, checked);

        const newFlags = Object.assign({}, record.data.extra_flags || {});

        if (!newFlags[recId]) {
            newFlags[recId] = [];
        }

        if (checked) {
            if (!newFlags[recId].includes(fieldName)) {
                newFlags[recId].push(fieldName);
            }
        } else {
            newFlags[recId] = newFlags[recId].filter(f => f !== fieldName);
        }

        // ✅ Always keep alphabetically sorted
        newFlags[recId] = newFlags[recId].sort((a, b) => a.localeCompare(b));

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
