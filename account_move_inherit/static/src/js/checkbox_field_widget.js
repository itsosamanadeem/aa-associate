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
    useEffect
} from "@odoo/owl";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class InvoiceLineListRendererWithCheckbox extends ListRenderer {
    static template = "account_move_inherit.ListRendererWithFooterCheckbox"
    static components = {
        CheckBox
    }
    setup() {
        super.setup()
        console.log('inherited', this.props);
        onWillRender(() => {
        })
        this.titleField = "name";
        useEffect(
            (editedRecord) => this.focusToName(editedRecord),
            () => [this.editedRecord]
        )

    }
    onToggle(ev) {
        console.log("test");
        const checked = ev.target.checked;
        console.log(`Checkbox toggled for ${column.name} on record ${record.id}:`, checked);


        // const record = this.props.record;
        // const fieldName = this.props.name;
        // const checked = ev.target.checked;

        // const newFlags = Object.assign({}, record.data.extra_flags || {});
        // newFlags[fieldName] = checked;

        // record.update({ extra_flags: newFlags });
    }
    focusToName(editRec) {
        if (editRec && editRec.isNew && this.isSectionOrNote(editRec)) {
            const col = this.columns.find((c) => c.name === this.titleField);
            this.focusCell(col, null);
        }
    }

    isSectionOrNote(record = null) {
        record = record || this.record;
        return ['line_section', 'line_note'].includes(record.data.display_type);
    }

    getRowClass(record) {
        const existingClasses = super.getRowClass(record);
        return `${existingClasses} o_is_${record.data.display_type}`;
    }

    getCellClass(column, record) {
        const classNames = super.getCellClass(column, record);
        if (this.isSectionOrNote(record) && column.widget !== "handle" && column.name !== this.titleField) {
            return `${classNames} o_hidden`;
        }
        return classNames;
    }

    getColumns(record) {
        const columns = super.getColumns(record);
        if (this.isSectionOrNote(record)) {
            return this.getSectionColumns(columns);
        }
        return columns;
    }

    getSectionColumns(columns) {
        const sectionCols = columns.filter((col) => col.widget === "handle" || col.type === "field" && col.name === this.titleField);
        return sectionCols.map((col) => {
            if (col.name === this.titleField) {
                return { ...col, colspan: columns.length - sectionCols.length + 1 };
            } else {
                return { ...col };
            }
        });
    }
}
export class InvoiceLineOne2ManyWithCheckbox extends X2ManyField {
    static components = {
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

