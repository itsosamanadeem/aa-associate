/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { formatCurrency } from "@web/core/currency";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";

export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog, Many2XAutocomplete };
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
        application_number: { type: Object, optional: true },
    };

    setup() {

        this.orm = useService("orm");
        this.notification = useService("notification");

        this.state = useState({
            selectedIds: [],
            variantList: this.props.variants.map(v => {
                return {
                    id: v.id,
                    name: v.name,
                    price: v.price,
                    imageUrl: `/web/image/product.product/${v.product_id}/image_256`,
                    product_id: v.product_id,
                };
            }),
            totalPrice: 0,
            selected_currency_id: null,
            selected_currency_name: "",
        });

        if (this.props.variants.length) {
            this.imageUrl = `/web/image/product.product/${this.props.variants[0].product_id}/image_256`;
            this.product_name = this.props.variants[0].product_name;
            this.attribute_name = this.props.variants[0].attribute_name;
        }

        this.selectVariant = this.selectVariant.bind(this);
        this.updateApplicationNumber = this.updateApplicationNumber.bind(this);

        onWillStart(async () => {
            if (!this.state.selected_currency_id && this.props.currency_id) {
                const currency = await this.orm.call("res.currency", "read", [['active','=',true], ["id", "name"]]);
                if (currency?.length) {
                    this.state.selected_currency_id = currency[0].id;
                    this.state.selected_currency_name = currency[0].name;
                }
            }
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

    get Many2XAutocompleteProps() {
        return {
            resModel: "res.currency",
            fieldString: _t("Currency"),
            getDomain: () => [["active", "=", true]],
            update: this.onCurrencySelect.bind(this),
            activeActions: {},
            placeholder: _t("Select a currency..."),
            value: this.state.selected_currency_name || "",
        }
    }
    onCurrencySelect(record) {
        console.log('this is the record', record.id);

        this.state.selected_currency_id = record?.id || false;
        this.state.selected_currency_name = record?.display_name || "";
        console.log("Selected Currency:", this.state.selected_currency_id);
    }
    updateApplicationNumber(variantId, value) {
        const variant = this.state.variantList.find(v => v.id === variantId);
        if (variant) {
            variant.applicationNumber = value || 0;
            // console.log("Updating application number for variant", variant.id, variant.applicationNumber);
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

    getProductTotalPrice() {
        const total = this.state.totalPrice;
        return formatCurrency(total, this.props.currency_id);
    }

    async confirm() {
        const total = this.state.totalPrice;

        await this.orm.call(
            "account.move.line",
            "update_price_unit",
            [[this.props.line_id], {
                price: total,
                variant_price: this.state.variantList[1].price,
                selected_variant_ids: this.state.selectedIds,
                selected_variant_names: this.state.variantList
                    .filter(v => this.state.selectedIds.includes(v.id))
                    .map(v => v.name),
                // active_currency_id: this.state.selected_currency_id,
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
