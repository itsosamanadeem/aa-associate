/** odoo-module **/

import { SaleOrderLineProductField } from "@sale/js/sale_product_field";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { Many2OneField, many2OneField } from "@web/views/fields/many2one/many2one_field";

export class AccountMoveLineProductField extends Many2OneField {
    static template = "account_move_inherit.InvoiceProductField";
    static components = {
        ...Many2OneField.components,
    };
    setup() {
        super.setup()
        console.log("AccountMoveLineProductField setup called", this.props.record.data.product_id[0]);
        // console.log("AccountMoveLineProductField setup called", this.props);
        this.actionService = useService("action");

    }

    async onEditConfiguration() {
        const product_id = this.props.record.data.product_id?.[0];
        if (!product_id) {
            console.warn("No product selected for configuration.");
            return;
        }
        const action = await rpc("/open_variant_price_wizard", { product_id });
        if (!action) {
            console.error("No action returned from server");
            return;
        }
        this.actionService.doAction(action);
    }

}
export const accountMoveLineProductField = {
    ...many2OneField,
    listViewWidth: [240, 400],
    component: AccountMoveLineProductField,
};
registry.category("fields").add("invoice_product_many2one", accountMoveLineProductField);
