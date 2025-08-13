/** odoo-module **/
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";

export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog };
    static props = {
        variants: { type: Array, required: true },
        onSelect: { type: Function, optional: true }, // callback for selected variant
        close: Function
    };

    setup() {
        console.log("Variants in Dialog:", this.props.variants);

        // Prepare variant display data
        this.variantList = this.props.variants.map(v => ({
            id: v.id,
            name: v.name,
            price: v.price,
            imageUrl: `/web/image/product.product/${v.id}/image_256`
        }));

        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    async selectVariant(variant) {
        try {
            if (this.props.onSelect) {
                await this.props.onSelect(variant);
            }
            this.notification.add(`Variant "${variant.name}" selected`, { type: "success" });
            this.close();
        } catch (error) {
            this.notification.add("Error selecting variant", { type: "danger" });
            console.error(error);
        }
    }

    close() {
        this.props.close();
    }
}
