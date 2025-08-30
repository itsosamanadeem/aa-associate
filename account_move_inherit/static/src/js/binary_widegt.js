/** @odoo-module **/

import { registry } from "@web/core/registry";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";
import { CheckboxCheck } from "./checkbox_field_widget";


export class UploadField extends BinaryField {
    static template = "account_move_inherit.UploadField";
    static components ={
        CheckboxCheck
    }
    setup(){
        super.setup()
    }
}

export const uploadField = {
    ...binaryField,
    component: UploadField,
};

registry.category("fields").add("upload", uploadField);
