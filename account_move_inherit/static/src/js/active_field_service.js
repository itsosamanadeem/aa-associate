/** account_move_inherit/static/src/js/active_fields_service.js **/
import { registry } from "@web/core/registry";

export const activeFieldsService = {
    dependencies: [],
    start() {
        let state = {};  // {line_id: {field_name: true/false}}

        return {
            getState: () => state,
            toggle(lineId, fieldName, value) {
                if (!state[lineId]) {
                    state[lineId] = {};
                }
                state[lineId][fieldName] = value;
            },
        };
    },
};

registry.category("services").add("active_fields_service", activeFieldsService);
