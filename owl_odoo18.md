# 🚀 How to Create a Public OWL Component in Odoo 18
How to create a public OWL component in Odoo 18. It includes both **Spanish and English** notes 

This guide will walk you through the process of creating a public component using the OWL (Odoo Web Library) framework in Odoo 18.

### 💡 **New Features in OWL Framework (Odoo >=18)**
- **Changelog**: Always review the official changelog to stay updated.
- **No need for `owl="1"` in templates**.
- **No longer necessary to declare `/** @odoo-module */` in JS files**.
- **QWeb `foreach` now requires a mandatory `t-key` attribute**.
- **Use `t-out` instead of `t-esc` for printing values**.
- **Assets should now be loaded in `assets_frontend` for public components**. Example in the `manifest` file:
  ```json
  "assets": {
    "web.assets_frontend": [
      "elearning_portal/static/src/components/subscribed_courses.js",
      "elearning_portal/static/src/components/subscribed_courses.xml"
    ]
  }
  ```

---

## 🛠️ Step-by-Step Guide to Create the OWL Component

### 1. 📦 **Creating the Manifest File**

The `manifest.json` file defines the module and its dependencies. Here's an example manifest for our eLearning portal component:

```json
{
    "name": "My eLearning Portal Component",
    "author": "CampusCleverit",
    "website": "https://campuscleverit.es",
    "version": "18.0.0.1.0",
    "summary": "Displays subscribed eLearning courses on the portal using OWL",
    "category": "Portal/eLearning",
    "depends": [
        "portal",
        "website_slides",
        "web"
    ],
    "data": [
        "views/portal_template.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "elearning_portal/static/src/components/*.js",
            "elearning_portal/static/src/components/*.xml"
        ]
    },
    "installable": true,
    "application": false,
    "auto_install": false,
    "license": "LGPL-3"
}
```

### 2. 📄 **JavaScript File - OWL Component**

Create the OWL component using JavaScript. This component will handle the logic to load and display the subscribed courses for a user.

- **Key Libraries**:
  - `@odoo/owl`: For OWL components.
  - `@web/core/registry`: For registering components.
  - `@web/core/network/rpc`: To make RPC calls to the server.

Here is an example of the `subscribed_courses.js`:

```js
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

console.log("elearning_portal: subscribed_courses.js loaded");

export class SubscribedCourses extends Component {
  static template = "elearning_portal.SubscribedCoursesTemplate";

  static props = {
    partnerId: { type: [Number, Boolean] },
  };

  setup() {
    this.state = useState({
      courses: [],
      isLoading: true,
      error: null,
    });

    onWillStart(async () => {
      if (!this.props.partnerId) {
        console.warn("Partner ID not provided.");
        this.state.isLoading = false;
        this.state.error = "Could not identify the user.";
        return;
      }
      await this.loadSubscribedCourses();
    });
  }

  async loadSubscribedCourses() {
    this.state.isLoading = true;
    this.state.error = null;
    try {
      const result = await rpc("/my_portal/subscribed_courses", {
        partner_id: this.props.partnerId,
      });
      this.state.courses = result;
      console.log("Courses loaded:", this.state.courses);
    } catch (err) {
      console.error("Error loading subscribed courses:", err);
      this.state.error = "An error occurred while loading your courses.";
    } finally {
      this.state.isLoading = false;
      const h3_it = document.querySelector("h3.h3_portal_courses");
      h3_it.textContent = `My Courses (${this.state.courses.length})`;
    }
  }
}

registry
  .category("public_components")
  .add("elearning_portal.SubscribedCourses", SubscribedCourses);
```

### 3. 📑 **Component Template (QWeb)**

In the `subscribed_courses.xml`, define the template for the component.

```xml
<templates xml:space="preserve">
    <t t-name="elearning_portal.SubscribedCoursesTemplate">
        <div class="subscribed-courses-list">
            <t t-if="state.isLoading">
                <div class="text-center text-muted py-3">
                    <i class="fa fa-spinner fa-spin me-1"/> Loading courses...
                </div>
            </t>

            <t t-elif="state.error">
                <div class="alert alert-danger" role="alert">
                    <t t-esc="state.error"/>
                </div>
            </t>

            <t t-elif="state.courses.length > 0">
                <ul class="list-group">
                    <t t-foreach="state.courses" t-as="course" t-key="course.id">
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <t t-esc="course.name"/>
                            <a t-attf-href="/slides/{{ course.id }}" class="btn btn-sm btn-primary">
                                Go to course <i class="fa fa-arrow-right"/>
                            </a>
                        </li>
                    </t>
                </ul>
            </t>

            <t t-else="">
                <div class="alert alert-info" role="alert">
                    You are not subscribed to any courses yet.
                </div>
            </t>
        </div>
    </t>
</templates>
```

### 4. 🖥️ **Backend - Controller Endpoint**

Now, let's create the controller to handle the RPC call to retrieve the courses subscribed by the user. This code resides in the `portal_elearning_controller.py` file.

```python
import odoo
import odoo.http as http
from odoo.http import request

class PortalElearningController(http.Controller):
    @http.route("/my_portal/subscribed_courses", type="json", auth="user", website=True)
    def get_subscribed_courses(self, partner_id=None, **kw):
        current_user_partner_id = request.env.user.partner_id.id
        if not partner_id or partner_id != current_user_partner_id:
            return []
        return self._fetch_courses_for_partner(partner_id)

    def _fetch_courses_for_partner(self, partner_id):
        try:
            subscriptions = (
                request.env["slide.channel.partner"]
                .sudo()
                .search([("partner_id", "=", partner_id)])
            )
            channel_ids = subscriptions.mapped("channel_id").ids
            courses = (
                request.env["slide.channel"]
                .sudo()
                .search_read([("id", "in", channel_ids)], ["id", "name"])
            )
            return courses
        except Exception as e:
            odoo.exceptions.UserError(f"Error fetching subscribed courses: {e}")
            return []
```

### 5. 🖧 **Portal Template (XML)**

Finally, modify the portal template to embed the OWL component where the courses should appear.

```xml
<odoo>
    <template id="portal_my_home_inherited_elearning" inherit_id="portal.portal_my_home">
        <xpath expr="//*[hasclass('o_portal_my_home')]" position="inside">
            <div class="mt-4">
                <h3 class="h3_portal_courses">My Courses (0)</h3>
                <t t-set="partner_id" t-value="sales_user.partner_id"/>
                <owl-component
                        name="elearning_portal.SubscribedCourses"
                        t-att-props="json.dumps({'partnerId': partner_id.id if partner_id else False })"/>
            </div>
        </xpath>
    </template>
</odoo>
```

### 🎉 **Congratulations!**

Now you have successfully created a public OWL component that displays a list of subscribed eLearning courses for the portal user.

---

### 📌 **Important Notes:**
- Make sure you **restart your Odoo server** after any code changes.
- The **`assets_frontend`** section in the manifest is crucial to ensure the OWL component is loaded on the frontend.
- Always check the **browser console** for potential errors during development.
- **Security**: Always validate inputs on the server-side to prevent unauthorized access.

Happy coding! 💻✨
