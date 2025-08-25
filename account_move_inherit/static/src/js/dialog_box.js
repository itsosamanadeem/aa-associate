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
                applicationNumber: 0,
            })),
            totalPrice: 0,
        });

        if (this.props.variants.length) {
            this.imageUrl = `/web/image/product.product/${this.props.variants[0].product_id}/image_256`;
            this.product_name = this.props.variants[0].product_name;
        }

        if (this.props.variants.length) {
            this.attribute_name = this.props.variants[0].attribute_name;
        }

        this.orm = useService("orm");
        this.notification = useService("notification");
        this.selectVariant = this.selectVariant.bind(this);
        this.updateApplicationNumber = this.updateApplicationNumber.bind(this);

        onWillStart(() => {
            if (this.props.selected_variant_ids?.length) {
                this.state.selectedIds = [...this.props.selected_variant_ids];
                this.state.totalPrice = this.state.variantList
                    .filter(v => this.state.selectedIds.includes(v.id))
                    .reduce((sum, v) => sum + parseFloat(v.price || 0), 0);
            }

            const selectedNames = this.state.variantList
                .filter(v => this.state.selectedIds.includes(v.id))
                .map(v => v.name);

            if (this.props.onConfirm) {
                this.props.onConfirm({
                    ids: this.state.selectedIds,
                    names: selectedNames,
                });
            }
        });
    }
    updateApplicationNumber(variantId, value) {
        const variant = this.state.variantList.find(v => v.id === variantId);
        if (variant) {
            variant.applicationNumber = parseInt(value || 0);
        }
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
    arraysEqual(arr1, arr2) {
        if (arr1.length !== arr2.length) return false;
        return arr1.every(val => arr2.includes(val));
    }
    getRawTotalPrice() {
        const originalIds = this.props.selected_variant_ids || [];
        const currentIds = this.state.selectedIds;

        // Variants that were added beyond the original
        const newlyAdded = this.state.variantList.filter(
            v => currentIds.includes(v.id) && !originalIds.includes(v.id)
        );

        // Variants that were removed compared to original
        const removed = this.state.variantList.filter(
            v => originalIds.includes(v.id) && !currentIds.includes(v.id)
        );

        let total = parseFloat(this.props.product_subtotal) || 0;

        // Add prices for new variants
        total += newlyAdded.reduce((sum, v) => sum + parseFloat(v.price || 0), 0);

        // Subtract prices for removed variants
        total -= removed.reduce((sum, v) => sum + parseFloat(v.price || 0), 0);

        return total;
    }

    getProductTotalPrice() {
        const total = this.getRawTotalPrice();
        return formatCurrency(total, this.props.currency_id);
    }

    async confirm() {
        const total = this.getRawTotalPrice();

        await this.orm.call(
            "account.move.line",
            "update_price_unit",
            [[this.props.line_id], {
                price: total,
                selected_variant_ids: this.state.selectedIds,
                selected_variant_names: this.state.variantList
                    .filter(v => this.state.selectedIds.includes(v.id))
                    .map(v => v.name),
                application_numbers: this.state.variantList
                    .filter(v => this.state.selectedIds.includes(v.id))
                    .map(v => ({ id: v.id, applicationNumber: v.applicationNumber })),  // <--- NEW
            }]
        );

        this.notification.add("Price and selected variants updated successfully!", { type: "success" });
        window.location.reload();
        this.close();
    }

    close() {
        window.location.reload();
        this.props.close();
    }
}
