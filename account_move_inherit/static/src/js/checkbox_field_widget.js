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

        const priority = {
            product_id: 1,
            product_template_id: 2,
            trademark_id:3,
            application_variant_data:4,
            opposition_number:5,
            registation_no:5,
            suit_number:6,
            appeal_number:7,
            rectification_number:8,
            filing_date:9,
            country_id:10,
            city_selection:11,
            log_attachment_id: 12,
            price_subtotal: 9999, 
        };

        newFlags[recId] = newFlags[recId].sort((a, b) => {
            const pa = priority[a] || 100;  
            const pb = priority[b] || 100;
            if (pa !== pb) {
                return pa - pb;  
            }
            return a.localeCompare(b); 
        });

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
