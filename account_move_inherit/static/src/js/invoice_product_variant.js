/** odoo-module **/

import { Many2OneField, many2OneField } from "@web/views/fields/many2one/many2one_field";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { ProductVariantDialog } from "./dialog_box";

export class AccountMoveLineProductField extends Many2OneField {
    static template = "account_move_inherit.InvoiceProductField";
    
    setup() {
        super.setup();
        this.actionService = useService("action");
        this.dialog = useService("dialog");
        this.orm = useService("orm")
        console.log(this.props.record);
    }

    async onEditConfiguration() {
        const product_tmpl_id = this.props.record.data.product_template_id?.[0];
        if (!product_tmpl_id) {
            console.warn("No product template selected for configuration.");
            return;
        }

        const variants = await rpc("/get_product_variants", { product_tmpl_id });

        if (!variants || variants.length === 0) {
            console.error("No variants found for product");
            return;
        }

        // Open custom dialog
        this.dialog.add(ProductVariantDialog, {
            variants,
            close: () => {
                this.actionService.doAction({ type: 'ir.actions.act_window_close' });
            },
            product_subtotal: this.props.record.data.price_subtotal,
            price_info: this.props.record.data.price_info,
            currency_id: this.props.record.data.currency_id[0],
        });
    }
}

export const accountMoveLineProductField = {
    ...many2OneField,
    listViewWidth: [240, 400],
    component: AccountMoveLineProductField,
};

registry.category("fields").add("invoice_product_many2one", accountMoveLineProductField);
