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
        price_info: { type: Object, optional: true },
        currency_id: { type: Number, optional: true },
        line_id: { type: Number, optional: true },
        selected_ptav_ids: { type: Array, optional: true },   // ✅ preload prop
    };

    setup() {
        // expose formatCurrency to the template
        this.formatCurrency = formatCurrency;
        onWillStart(async () => {
            const savedVariants = await this.orm.call(
                    "account.move.line",
                    "read",
                    [[this.props.line_id], ["selected_ptav_ids"]]
                );

            const selectedIdsFromDB = savedVariants[0]?.selected_variant_ids || [];
            
            this.state = useState({
                selectedIds: selectedIdsFromDB,  // ✅ pre-check
                variantList: this.props.variants.map(v => ({
                    id: v.id,                 // PTAV id
                    name: v.name,
                    price: v.price,
                    imageUrl: `/web/image/product.product/${v.product_id}/image_256`,
                })),
                totalPrice: 0,
            });
        });

        if (this.props.variants.length) {
            this.imageUrl = `/web/image/product.product/${this.props.variants[0].product_id}/image_256`;
            this.product_name = this.props.variants[0].product_name;
        }

        this.orm = useService("orm");
        this.notification = useService("notification");

        // compute initial total if preselected
        this.state.totalPrice = this.state.variantList
            .filter(v => this.state.selectedIds.includes(v.id))
            .reduce((sum, v) => sum + (parseFloat(v.price) || 0), 0);

        this.selectVariant = this.selectVariant.bind(this);
    }

    selectVariant(variant) {
        const idx = this.state.selectedIds.indexOf(variant.id);
        if (idx === -1) this.state.selectedIds.push(variant.id);
        else this.state.selectedIds.splice(idx, 1);

        this.state.totalPrice = this.state.variantList
            .filter(v => this.state.selectedIds.includes(v.id))
            .reduce((sum, v) => sum + (parseFloat(v.price) || 0), 0);
    }

    getProductTotalPrice() {
        const subtotal = parseFloat(this.props.product_subtotal) || 0;
        const total = (this.state.totalPrice || 0) + subtotal;
        return formatCurrency(total, this.props.currency_id);
    }

    async confirm() {
        const subtotal = parseFloat(this.props.product_subtotal) || 0;
        const total = (this.state.totalPrice || 0) + subtotal;

        await this.orm.call(
            "account.move.line",
            "update_price_unit",
            [[this.props.line_id], {
                price: total,
                selected_ptav_ids: this.state.selectedIds,   // ✅ persist PTAVs
            }]
        );

        this.notification.add("Updated successfully!", { type: "success" });
        this.close();
    }

    close() {
        this.props.close();
    }
}
