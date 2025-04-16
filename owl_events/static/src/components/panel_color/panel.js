import {useService} from "@web/core/utils/hooks";
import {Component, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import ButtonColorComponent from "../button_color/button_color";

export class PanelColorComponent extends Component {
    static template = "owl_events.PanelColorComponent";
    static components = {ButtonColorComponent};

    setup() {
        super.setup()
        this.onColorSelected = this.onColorSelected.bind(this)
        this.notification = useService("notification");
        this.state = useState({
            message: null,
            selectedColor: 'light', // Color inicial (default color)
            availableColors: ['danger', 'dark', 'success', 'warning', 'light'],
        });
    }

    onColorSelected(color) {

        this.state.message = "🐓 I'm the Parent Component, updating color to " + color;
        const msg = this.state.message;

        this.notification.add(msg, {
            title: "Parent",
            type: "warning",
            sticky: false,
        });


        setTimeout(() => {
            this.state.message = null;
            this.state.selectedColor = color

        }, 4000)

    }
}

registry
    .category("public_components")
    .add(
        "owl_events.PanelColorComponent",
        PanelColorComponent
    );
