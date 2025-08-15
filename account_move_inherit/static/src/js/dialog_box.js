/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { formatCurrency } from "@web/core/currency";

export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog };
    static props = {
        variants: { type: Array },  
        close: Function,
        product_subtotal: { type: Number, optional: true },
        price_info: { type: String, optional: true },
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
            totalPrice: 0,
            product_total_price: 0,
        });
        
        console.log(this);
        
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
        this.state.totalPrice = formatCurrency(this.state.variantList
            .filter(v => this.state.selectedIds.includes(v.id))
            .reduce((sum, v) => sum + parseFloat(v.price || 0), 0), this.env.currency.id);

        console.log("Selected IDs:", this.state.selectedIds);
        console.log("Total Price:", this.state.totalPrice);
    }

    getProductTotalPrice() {
        return formatCurrency(()=>{
            this.state.product_total_price = this.state.variantList
                .filter(v => this.state.selectedIds.includes(v.id))
                .reduce((sum, v) => sum + parseFloat(v.price || 0), 0);
            return this.state.product_total_price + (this.props.product_subtotal || 0);
        }, this.env.currency.id);
    }
    async confirm() {
        if (!this.state.selectedIds.length) {
            this.notification.add("Please select at least one variant", { type: "warning" });
            return;
        }
        const selected = this.state.variantList.filter(v => this.state.selectedIds.includes(v.id));
        this.props.close(selected);
    }

    close() {
        this.props.close();
    }
}
