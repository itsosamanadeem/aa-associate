/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import {
    productLabelSectionAndNoteOne2Many,
    ProductLabelSectionAndNoteOne2Many,
    ProductLabelSectionAndNoteListRender,
} from '@account/components/product_label_section_and_note_field/product_label_section_and_note_field';
import {
    SectionAndNoteListRenderer,
    sectionAndNoteFieldOne2Many,
} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";

export class InvoiceLineListRendererWithCheckbox extends ProductLabelSectionAndNoteOne2Many {
    setup() {
        super.setup()
        console.log('inherited');

        renderBodyCell({ column, record, isAnchor, rowIndex, colIndex }) {
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
}
export const invoiceLineListRendererWithCheckbox = {
    ...x2ManyField,
    component: InvoiceLineListRendererWithCheckbox,
    additionalClasses: sectionAndNoteFieldOne2Many.additionalClasses,
};

registry
    .category("fields")
    .add("invoiceLine_list_renderer_with_checkbox", invoiceLineListRendererWithCheckbox);

