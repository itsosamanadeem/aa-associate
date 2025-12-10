/** @odoo-module **/
import { MrpDisplayRecord } from '@mrp_workorder/src/mrp_display';

export class InheritMrpDisplayRecord extends MrpDisplayRecord {
    setup() {
        console.log(this.props);
        
    }
}
