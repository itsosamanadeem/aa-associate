/** odoo-module **/

import { SaleOrderLineProductField } from "@sale/js/sale_product_field";
import { registry } from "@web/core/registry";

export class AccountMoveLineProductField extends SaleOrderLineProductField {
    static template = "account_move_inherit.InvoiceProductField";
    setup() {
        super.setup()
    }
}

registry.category("fields").add("invoice_product_many2one", AccountMoveLineProductField);
