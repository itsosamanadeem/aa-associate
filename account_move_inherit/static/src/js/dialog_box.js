/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";

export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog };
    static props = {
        variants: { type: Array },  
        close: Function
    };

    setup() {

        this.props.variants.forEach(variant => {
            this.imageUrl = `/web/image/product.product/${variant.product_id}/image_256`;
        });
        
        this.props.variants.forEach(variant => {
            this.product_name = variant.product_name;
        });

        this.state = useState({
            selectedId: null,
            variantList: this.props.variants.map(v => ({
                id: v.id,
                name: v.name,
                price: v.price,
                imageUrl: `/web/image/product.product/${v.product_id}/image_256`
            }))
        });
        console.log(this.state.variantList);
        
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    selectVariant(variant) {
        this.state.selectedId = variant.id;
    }

    async confirm() {
        if (!this.state.selectedId) {
            this.notification.add("Please select a variant", { type: "warning" });
            return;
        }
        const selected = this.state.variantList.find(v => v.id === this.state.selectedId);
        console.log("Selected Variant:", selected);
        this.props.close(selected); // send back selected variant
    }

    close() {
        this.props.close();
    }
}
