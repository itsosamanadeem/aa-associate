/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
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
        price_info: { type: Object, optional: true },
        currency_id: { type: Number, optional: true },
        line_id: { type: Number, optional: true },
        onConfirm: { type: Function },
        product_id: { type: Number, optional: true },
        selected_variant_ids: { type: Array, optional: true },
    };

    setup() {
        this.state = useState({
            selectedIds: [],
            variantList: this.props.variants.map(v => ({
                id: v.id,
                name: v.name,
                price: v.price,
                imageUrl: `/web/image/product.product/${v.product_id}/image_256`,
                product_id: v.product_id,
            })),
            totalPrice: 0,
        });

        if (this.props.variants.length) {
            this.imageUrl = `/web/image/product.product/${this.props.variants[0].product_id}/image_256`;
            this.product_name = this.props.variants[0].product_name;
        }

        this.orm = useService("orm");
        this.notification = useService("notification");
        this.selectVariant = this.selectVariant.bind(this);

        onWillStart(() => {
            if (this.props.selected_variant_ids?.length) {
                this.state.selectedIds = [...this.props.selected_variant_ids];
                this.state.totalPrice = this.state.variantList
                    .filter(v => this.state.selectedIds.includes(v.id))
                    .reduce((sum, v) => sum + parseFloat(v.price || 0), 0);
            }
        });
    }

    selectVariant(variantId) {
        const index = this.state.selectedIds.indexOf(variantId);
        if (index === -1) {
            this.state.selectedIds.push(variantId);
        } else {
            this.state.selectedIds.splice(index, 1);
        }

        this.state.totalPrice = this.state.variantList
            .filter(v => this.state.selectedIds.includes(v.id))
            .reduce((sum, v) => sum + parseFloat(v.price || 0), 0);
    }

    getProductTotalPrice() {
        const total = this.state.totalPrice + (parseFloat(this.props.product_subtotal) || 0);
        return formatCurrency(total, this.props.currency_id);
    }

    async confirm() {
        const total = this.state.totalPrice + (parseFloat(this.props.product_subtotal) || 0);

        await this.orm.call(
            "account.move.line",
            "update_price_unit",
            [[this.props.line_id], {
                price: total,
                selected_variant_ids: this.state.selectedIds,
            }]
        );

        const selectedNames = this.state.variantList
            .filter(v => this.state.selectedIds.includes(v.id))
            .map(v => v.name);

        if (this.props.onConfirm) {
            this.props.onConfirm({
                ids: this.state.selectedIds,
                names: selectedNames,   // ✅ send names to parent
            });
        }

        this.notification.add("Price and selected variants updated successfully!", { type: "success" });
        
        this.close();
    }

    close() {
        this.props.close();
    }
}
