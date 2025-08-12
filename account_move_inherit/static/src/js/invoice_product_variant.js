/** odoo-module **/

import { Many2OneField, many2OneField } from "@web/views/fields/many2one/many2one_field";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";

export class AccountMoveLineProductField extends Many2OneField {
    static template = "account_move_inherit.InvoiceProductVariantField";
    static components = { Dialog , Many2XAutocomplete};
    setup() {
        super.setup();
        this.actionService = useService("action");
        this.dialog = useService("dialog");
        this.orm = useService("orm")
    }

    async onEditConfiguration() {
        const product_tmpl_id = this.props.record.data.product_tmpl_id?.[0];
        // this.dialog.add(Dialog{
        //     product_tmpl_id: this.props.record.data.product_tmpl_id?.[0]
        // })
        if (!product_tmpl_id) {
            console.warn("No product template selected for configuration.");
            return;
        }
        const action = await rpc("/open_product_variants", { product_tmpl_id });
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
