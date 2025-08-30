/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import {
    sectionAndNoteFieldOne2Many,
} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";

/**
 * Step 1: Custom renderer extending SectionAndNoteListRenderer
 */
export class InvoiceLineListRendererWithCheckbox extends ListRenderer {
    
    renderBodyCell({ column, record, isAnchor, rowIndex, colIndex }) {
        console.log('inherited!!!!!!');
        const td = super.renderBodyCell({ column, record, isAnchor, rowIndex, colIndex });

        if (record.resModel === "account.move.line") {
            const fieldName = column.name;

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.style.marginLeft = "4px";
            checkbox.checked = record.data.extra_flags?.[fieldName] || false;

            checkbox.addEventListener("change", () => {
                const newFlags = Object.assign({}, record.data.extra_flags || {});
                newFlags[fieldName] = checkbox.checked;
                record.update({ extra_flags: newFlags });
            });

            td.appendChild(checkbox);
        }
        return td;
    }
}

/**
 * Step 2: Custom X2Many using our renderer
 */
export class InvoiceLineX2ManyWithCheckbox extends X2ManyField {
    static components = {
        ...X2ManyField.components,
        ListRenderer: InvoiceLineListRendererWithCheckbox,
    };
}

/**
 * Step 3: Register widget
 */
registry.category("fields").add("invoiceLine_list_renderer_with_checkbox", {
    ...x2ManyField,
    component: InvoiceLineX2ManyWithCheckbox,
    additionalClasses: sectionAndNoteFieldOne2Many.additionalClasses,
});
