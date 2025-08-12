/** odoo-module **/
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
export class ProductVariantDialog extends Component {
    static template = "account_move_inherit.ProductVariantDialog";
    static components = { Dialog };
    static props = {
        variants: { type: Array },  // required: list of variants
        close: { type: Function },  // injected by dialog service
    };
    setup() {
        // Variants are passed as props
        console.log("Variants in Dialog:", this.props.variants);
        this.actionService = useService("action");
    }
    close() {
        this.actionService.doAction({type: 'ir.actions.act_window_close'});
    }
}
