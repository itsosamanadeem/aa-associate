/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";

export class InvoiceLineListRendererWithCheckbox extends ListRenderer {
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

export class InvoiceLineX2ManyWithCheckbox extends X2ManyField {
    static components = {
        ...X2ManyField.components,
        ListRenderer: InvoiceLineListRendererWithCheckbox,
    }
}

registry.category("fields").add("invoice_line_x2many_checkbox", {
    ...x2ManyField,
    component: InvoiceLineX2ManyWithCheckbox,
});
