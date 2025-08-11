/** @odoo-module **/
import { registry } from "@web/core/registry";

registry.category("actions").add("custom.notification_reload", async function (env, action) {
    const { title, message, type, delay } = action.params;

    env.services.notification.add(message, {
        title: title || "Notice",
        type: type || "info",
        sticky: true,
    });

    setTimeout(() => {
        env.services.action.doAction({
            type: "ir.actions.client",
            tag: "reload",
        });
    }, delay || 500);
});
