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
        console.log('inherited', this.props.record);

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

