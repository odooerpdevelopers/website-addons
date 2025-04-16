# Odoo OWL Events - Parent-Child Communication

## Overview

This module demonstrates how to implement parent-child component communication in Odoo 18 using OWL (Odoo Web Library). The example shows a parent panel component that changes its background color based on events triggered by child button components.

<img src="./events.png" />

## Technical Features

- OWL Component Architecture
- Parent-Child Component Communication
- Event Handling in OWL
- Notification Service Integration
- Frontend Web Routes
- Public Component Registration

## Installation

### Prerequisites

- Odoo 18
- Basic knowledge of OWL framework

### Steps

1. Create a new module directory named `owl_events` in your Odoo addons path
2. Copy the files as described in the directory structure below
3. Install the module through Odoo's module installation interface

## Directory Structure

```
owl_events/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── views/
│   └── server_templates.xml
└── static/
    └── src/
        └── components/
            ├── panel_color/
            │   ├── parent.js
            │   └── parent.xml
            └── button_color/
                ├── button_color.js
                └── button_color.xml
```

## Module Files

### `__manifest__.py`

```python
{
    'name': 'Ejemplo de Eventos OWL',
    'version': '1.0',
    'summary': 'Ejemplo para demostrar la comunicación padre-hijo con eventos en OWL',
    'category': 'Tutorial',
    'author': 'Tu Nombre',
    'depends': ['web'],
    'data': [
        'views/server_templates.xml',  # Para el template que lanza el componente
    ],
    'assets': {
        'web.assets_frontend': [
            'owl_events/static/src/components/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
```

### `__init__.py` (Root)

```python
from . import controllers
```

### `controllers/__init__.py`

```python
from . import main
```

### `controllers/main.py`

```python
from odoo import http
from odoo.http import request

class OwlEventsController(http.Controller):
    @http.route('/owl_events', type='http', auth="public", website=True)
    def owl_events_page(self, **kw):
        return http.request.render('owl_events.owl_events_page')
```

### `views/server_templates.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <template id="owl_events_page" name="Página de Ejemplo de Eventos OWL">
        <t t-call="website.layout">
            <div id="wrap" class="oe_structure oe_empty">
                <div class="container shadow" style="width: 1200px; min-height: 600px; box-shadow: 2px">
                    <h2 class="text-center">OWL Events</h2>
                    <owl-component name="owl_events.PanelColorComponent"/>
                </div>
            </div>
        </t>
    </template>
</odoo>
```

### `static/src/components/panel_color/parent.js`

```javascript
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
            selectedColor: 'light', // Color inicial
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
```

### `static/src/components/panel_color/parent.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates>
    <div t-name="owl_events.PanelColorComponent" style="height: 500px;"
         t-attf-class="h-5 py-2 mb-2 bg-{{state.selectedColor}} text-center border border-5 rounded-4">
        <div class="mb-2">
            <h3 t-attf-class="text-center {{ state.selectedColor === 'dark' ? 'text-white' : 'text-dark' }}">Parent</h3>
            <!--<div class="alert alert-info text-center fade show mx-auto mt-2" t-attf-style="width: 500px; height: 50px; {{ state.message ? 'opacity:1' : 'opacity:0' }}">
                <span t-out="state.message"/>
            </div>-->
        </div>

        <div class="d-flex justify-content-center gap-3">
            <t t-foreach="state.availableColors" t-as="color" t-key="color_index">
                <ButtonColorComponent color="color" onColorSelected="onColorSelected" id="color_index"/>
            </t>
        </div>
    </div>
</templates>
```

### `static/src/components/button_color/button_color.js`

```javascript
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
```

### `static/src/components/button_color/button_color.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <div t-name="owl_events.ButtonColorComponent" class="m-2" t-att-data-id="props.id">
        <button t-attf-class="btn btn-lg btn-{{props.color}} border border-5" t-on-click="onClick">Child Component</button>
    </div>
</templates>
```

## Technical Explanation

### Component Architecture

This module demonstrates a parent-child component relationship:

1. **Parent Component** (`PanelColorComponent`): 
   - Acts as the container for multiple child components
   - Maintains state for the selected color
   - Changes its background color based on events from child components

2. **Child Component** (`ButtonColorComponent`):
   - Represents a colored button
   - Sends events to the parent when clicked
   - Receives configuration through props

### Event Communication Flow

1. User clicks a colored button (child component)
2. The child component displays a notification ("I'm the Child Component...")
3. After a 2-second delay, the child component calls the parent's `onColorSelected` method
4. The parent component displays a notification ("I'm the Parent Component...")
5. After a 4-second delay, the parent component updates its background color

### State Management

The parent component uses OWL's `useState` hook to manage reactive state:

```javascript
this.state = useState({
    message: null,
    selectedColor: 'light',
    availableColors: ['danger', 'dark', 'success', 'warning', 'light'],
});
```

When the state changes, OWL automatically re-renders the component.

### Props and Event Handler Passing

The parent passes two pieces of information to each child:
1. The `color` property that defines which color the button will be
2. The `onColorSelected` callback function that the child will call when clicked

```xml
<ButtonColorComponent color="color" onColorSelected="onColorSelected" id="color_index"/>
```

### Notification Service

Both components use Odoo's notification service to display messages:

```javascript
this.notification = useService("notification");

// Later when needed
this.notification.add(message, {
    title: "Parent",
    type: "warning",
    sticky: false,
});
```

### Public Component Registration

The parent component is registered as a public component to make it available on the frontend:

```javascript
registry
    .category("public_components")
    .add(
        "owl_events.PanelColorComponent",
        PanelColorComponent
    );
```

## Front-end Access

Once installed, you can access the component at:

```
https://your-odoo-site.com/owl_events
```

## Best Practices Used

1. **Component Composition**: Breaking UI into reusable components
2. **Unidirectional Data Flow**: Parent passes data down, child sends events up
3. **Prop Validation**: Using static props definition for type checking
4. **Service Injection**: Using the `useService` hook for accessing Odoo services
5. **State Management**: Using `useState` for reactive state

## Additional Resources

- [Odoo OWL Documentation](https://github.com/odoo/owl)
- [Odoo JavaScript Framework](https://www.odoo.com/documentation/18.0/developer/reference/frontend/javascript_framework.html)
- [Odoo Web Components](https://www.odoo.com/documentation/18.0/developer/reference/frontend/web_components.html)

## Troubleshooting

### Component Not Rendering

If the component isn't rendering on the frontend:

1. Check browser console for errors
2. Verify that the assets are properly loaded in the `__manifest__.py`
3. Ensure the component is properly registered in the public_components registry

### Event Handler Not Working

If clicking buttons doesn't change the parent's color:

1. Check the browser console for errors
2. Verify that the `onColorSelected` method is properly bound in the setup method
3. Ensure the child component is correctly passing the color to the parent

## Conclusion

This module demonstrates the powerful component model of OWL in Odoo 18. By understanding these patterns, you can build complex, interactive UIs with clean separation of concerns and proper component communication.
