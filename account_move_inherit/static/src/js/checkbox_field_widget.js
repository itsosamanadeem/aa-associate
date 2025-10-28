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

        console.log('checking out the seqeunce of the fields', this.props.archInfo.columns);
    }
    onFieldCheckboxToggle(record, fieldName, ev) {
        const checked = ev.target.checked;
        const recId = record.resId || record.id;
        // console.log('Toggle for', recId, fieldName, checked);

        let columnSequence = this.props.archInfo.columns
        let visible_columns = columnSequence.filter(col => !col.column_invisible);
        console.log("Visible columns:", visible_columns);

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
            product_id: 1,                 // Service
            trademark_id: 2,
            logo_attachment_id: 3,
            label_id: 4,
            x_studio_title_of_invention: 5,
            product_template_id: 6,        // Classes
            application_variant_data: 7,   // Application Number
            opposition_number: 8,
            registration_no: 9,
            suit_number: 10,
            appeal_number: 11,
            rectification_no: 12,
            filing_date: 13,
            country_id: 14,
            city_selection: 15,
            tax_amount: 9989,
            professional_fees: 9990,
            service_fee: 9991,
            offical_fees: 9992,
            fees_calculation: 9994,
            discount: 9995,
            tax_ids: 9996,
            price_total: 9998,
            price_unit: 9999,  
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
