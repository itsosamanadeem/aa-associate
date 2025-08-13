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
        this.state = useState({
            selectedIds: [],
            variantList: this.props.variants.map(v => ({
                id: v.id,
                name: v.name,
                price: v.price,
                imageUrl: `/web/image/product.product/${v.product_id}/image_256`
            })),
            totalPrice: 0
        });

        // Pick first variant's image & product name just for header
        if (this.props.variants.length) {
            this.imageUrl = `/web/image/product.product/${this.props.variants[0].product_id}/image_256`;
            this.product_name = this.props.variants[0].product_name;
        }

        this.orm = useService("orm");
        this.notification = useService("notification");

        this.selectVariant = this.selectVariant.bind(this);
    }

    selectVariant(variant) {
        const index = this.state.selectedIds.indexOf(variant.id);
        if (index === -1) {
            this.state.selectedIds.push(variant.id);
        } else {
            this.state.selectedIds.splice(index, 1);
        }

        // Recalculate total price
        this.state.totalPrice = this.state.variantList
            .filter(v => this.state.selectedIds.includes(v.id))
            .reduce((sum, v) => sum + parseFloat(v.price || 0), 0);

        console.log("Selected IDs:", this.state.selectedIds);
        console.log("Total Price:", this.state.totalPrice);
    }

    async confirm() {
        if (!this.state.selectedIds.length) {
            this.notification.add("Please select at least one variant", { type: "warning" });
            return;
        }
        const selected = this.state.variantList.filter(v => this.state.selectedIds.includes(v.id));
        const totalPrice = this.state.totalPrice;
        this.props.close({ selected, totalPrice }); // sending both
    }

    close() {
        this.props.close();
    }
}
