/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class InvoiceLineListRendererWithFieldCheckbox extends ListRenderer {
    static components = { ...ListRenderer.components, CheckBox };
    static recordRowTemplate = "account_move_inherit.ListRenderer.RecordRowWithCheckbox";
    static props = {
        ...standardFieldProps,
    }
    setup(){
        super.setup()
        // console.log('record!!!!', this.props);
        
    }
    onFieldCheckboxToggle(record, ev) {
        const rec = record
        const fieldName= this.props.name
        const checked = ev.target.checked;

        console.log('rec', rec, 'fieldName', fieldName, 'checked', checked);
        
        const newFlags = Object.assign({}, rec.data.extra_flags || {});
        newFlags[fieldName] = checked;

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
