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
import {
    Component,
    onMounted,
    onPatched,
    onWillPatch,
    onWillRender,
    useExternalListener,
    useRef,
} from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class InvoiceLineListRendererWithCheckbox extends ListRenderer {
    static template ="account_move_inherit.InvoiceLineListRendererWithCheckbox"
    static components={
        CheckBox
    }
    setup() {
        super.setup()
        onWillRender(()=>{
            console.log('inherited', this.props);
        })

    }
    onToggle(ev) {
        console.log("test");
        
        // const record = this.props.record;
        // const fieldName = this.props.name;
        // const checked = ev.target.checked;

        // const newFlags = Object.assign({}, record.data.extra_flags || {});
        // newFlags[fieldName] = checked;

        // record.update({ extra_flags: newFlags });
    }
}
export class InvoiceLineOne2ManyWithCheckbox extends X2ManyField{
    static components={
        ...X2ManyField.components,
        ListRenderer: InvoiceLineListRendererWithCheckbox
    }
}
export const invoiceLineRendererWithCheckbox = {
    ...x2ManyField,
    component: InvoiceLineOne2ManyWithCheckbox,
    // additionalClasses: sectionAndNoteFieldOne2Many.additionalClasses,
};

registry.category("fields").add("invoiceLine_list_renderer_with_checkbox", invoiceLineRendererWithCheckbox);

