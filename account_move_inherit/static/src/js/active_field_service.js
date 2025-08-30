/** account_move_inherit/static/src/js/active_fields_service.js **/
import { registry } from "@web/core/registry";

export const activeFieldsService = {
    dependencies: [],
    start() {
        let state = {}; 

        return {
            getState: () => state,
            toggle(lineId, fieldName, value) {
                console.log('line id', lineId, 'fieldName',fieldName, 'value', value);
                
                if (!state[lineId]) {
                    state[lineId] = {};
                }
                state[lineId][fieldName] = value;

                return state;
            },
        };
    },
};

registry.category("services").add("active_fields_service", activeFieldsService);
