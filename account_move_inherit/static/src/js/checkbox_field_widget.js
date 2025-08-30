/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";

export class InvoiceLineListRendererWithCheckbox extends ListRenderer {
    static template = "account_move_inherit.ListRendererWithCheckbox";
    setup(){
        super.setup()
        console.log("values ", this.props);
        
    }
    onToggle(record, ev) {
        console.log("Checkbox toggled for record", record.id, "checked?", ev.target.checked);
        // you can update the record if you want:
        // record.update({ my_checkbox: ev.target.checked });
    }
}

export class InvoiceLineOne2ManyWithCheckbox extends X2ManyField {
    static components = {
        ...X2ManyField.components,
        ListRenderer: InvoiceLineListRendererWithCheckbox,
    };
}

registry.category("fields").add("invoiceLine_list_renderer_with_checkbox", {
    ...x2ManyField,
    component: InvoiceLineOne2ManyWithCheckbox,
});
