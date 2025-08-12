/** odoo-module **/

import { SaleOrderLineProductField } from "@sale/js/sale_product_field";
import { registry } from "@web/core/registry";
import {
    ProductLabelSectionAndNoteField,
    productLabelSectionAndNoteField,
} from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field";

export class AccountMoveLineProductField extends ProductLabelSectionAndNoteField {
    static template = "account_move_inherit.InvoiceProductField";
    static props = {
        ...ProductLabelSectionAndNoteField.props,
        readonlyField: { type: Boolean, optional: true },
    };
    setup() {
        super.setup()
    }
}
export const accountMoveLineProductField = {
    ...productLabelSectionAndNoteField,
    component: AccountMoveLineProductField,
    extractProps(fieldInfo, dynamicInfo) {
        const props = productLabelSectionAndNoteField.extractProps(...arguments);
        props.readonlyField = dynamicInfo.readonly;
        return props;
    },
};
registry.category("fields").add("invoice_product_many2one", accountMoveLineProductField);
