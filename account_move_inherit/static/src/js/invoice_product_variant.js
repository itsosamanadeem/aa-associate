/** odoo-module **/

import { SaleOrderLineProductField } from "@sale/js/sale_product_field";
import { registry } from "@web/core/registry";
import {
    ProductLabelSectionAndNoteField,
    productLabelSectionAndNoteField,
} from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";

export class AccountMoveLineProductField extends ProductLabelSectionAndNoteField {
    static template = "account_move_inherit.InvoiceProductField";
    static props = {
        ...ProductLabelSectionAndNoteField.props,
        readonlyField: { type: Boolean, optional: true },
    };
    setup() {
        super.setup()
        console.log("AccountMoveLineProductField setup called", this.props.record.data.sequence);
        // console.log("AccountMoveLineProductField setup called", this.props);
        this.actionService = useService("action");

    }

    async onEditConfiguration() {
        const moveLineId = this.props.record.data.sequence;
        const action = await rpc("/open_variant_price_wizard", { move_line_id: moveLineId });
        this.actionService.doAction(action);
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
