import {useService} from "@web/core/utils/hooks";
import {Component} from "@odoo/owl";

export default class ButtonColorComponent extends Component {
    static template = "owl_events.ButtonColorComponent";
    static props = {
        color: {type: String},
        id: {type: Number},
        onColorSelected: {type: Function}
    };

    setup() {
        super.setup()
        this.notification = useService("notification");
    }

    onClick() {
        const msg = "🐥 I'm the Child Component, requesting a color change";
        this.notification.add(msg, {
            title: "Child",
            type: "info",
            sticky: false,
        });
        setTimeout(() => {

            this.props.onColorSelected(this.props.color);  // Call to parent
        }, 2000)
    }
}
