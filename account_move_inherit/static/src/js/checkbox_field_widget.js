/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";

export class InvoiceLineRendererWithCheckbox extends ListRenderer {
    renderBodyCell({ column, record, isAnchor, rowIndex, colIndex }) {
        const td = super.renderBodyCell({ column, record, isAnchor, rowIndex, colIndex });

        // only apply on invoice lines
        if (record.model === "account.move.line") {
            const fieldName = column.name;

            // create checkbox
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.style.marginLeft = "5px";
            checkbox.checked = record.data.extra_flags?.[fieldName] || false;

            checkbox.addEventListener("change", () => {
                const newFlags = Object.assign({}, record.data.extra_flags || {});
                newFlags[fieldName] = checkbox.checked;
                record.update({ extra_flags: newFlags });  // updates in DB
            });

            td.appendChild(checkbox);
        }

        return td;
    }
}

registry.category("views").add("invoice_line_list_with_checkbox", {
    ...registry.category("views").get("list"),
    Renderer: InvoiceLineRendererWithCheckbox,
});
