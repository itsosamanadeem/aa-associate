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
        this.variantList = this.props.variants.map(v => ({
            id: v.id,
            name: v.name,
            price: v.price,
            image: v.product_image,
            imageUrl: `/web/image/product.product/${v.id}/image_256`
        }));
        this.actionService = useService("action");
    }

    close() {
        this.props.close();
    }
}
