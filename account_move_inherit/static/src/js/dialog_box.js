/** odoo-module **/
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog };
    static props = {
        variants: { type: Array },  // required: list of variants
        close: Function
    };
    setup() {
        // Variants are passed as props
        console.log("Variants in Dialog:", this.props.variants);
        this.props.variants.forEach(variant => {
            this.image = variant.product_image; // Assuming each variant has an image field
            this.id= variant.id; // Assuming each variant has an id field
            this.name = variant.name; // Assuming each variant has a name field
            this.price = variant.price; // Assuming each variant has a price field
            console.log("Variant:", variant);
        });
        this.actionService = useService("action");
    }
    close() {
        this.props.close();
    }
}
