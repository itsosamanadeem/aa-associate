/** odoo-module **/
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog };

    setup() {
        // Variants are passed as props
        console.log("Variants in Dialog:", this.props.variants);
    }
}
