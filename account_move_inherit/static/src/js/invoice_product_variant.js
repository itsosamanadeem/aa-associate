/** odoo-module **/

import { Many2OneField, many2OneField } from "@web/views/fields/many2one/many2one_field";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class AccountMoveLineProductVariantField extends Many2OneField {
    static template = "account_move_inherit.InvoiceProductVariantField";

    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    async onShowVariants() {
        const product_tmpl_id = this.props.record.data.product_tmpl_id?.[0];
        if (!product_tmpl_id) {
            console.warn("No product template found.");
            return;
        }

        const variants = await rpc("/get_product_variants", { product_tmpl_id });
        if (!variants.length) {
            this.dialogService.add(Dialog, { title: "No Variants", body: "This product has no variants." });
            return;
        }

        this.dialogService.add(Dialog, {
            title: "Product Variants",
            body: {
                Component: {
                    template: "account_move_inherit.ProductVariantDialogTable",
                    props: { variants },
                },
            },
        });
    }
}

export const accountMoveLineProductVariantField = {
    ...many2OneField,
    listViewWidth: [240, 400],
    component: AccountMoveLineProductVariantField,
};

registry.category("fields").add("invoice_product_many2one", accountMoveLineProductVariantField);
