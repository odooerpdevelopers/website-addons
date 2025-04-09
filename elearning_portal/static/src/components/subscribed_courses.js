import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

console.log(" elearning_portal: subscribed_courses.js cargado");

export class SubscribedCourses extends Component {
  static template = "elearning_portal.SubscribedCoursesTemplate"; // Component Template (QWeb)

  // Props que esperamos recibir desde el QWeb del servidor
  static props = {
    partnerId: { type: [Number, Boolean] }, // Puede ser el ID o False si no hay usuario/partner
  };

  setup() {
    console.log("elearning_portal: subscribed_courses.js setup overrided");

    // State to store the courses and loading status
    this.state = useState({
      courses: [],
      isLoading: true,
      error: null,
    });

    // Hook that runs before the first render
    onWillStart(async () => {
      if (!this.props.partnerId) {
        console.warn("ID de Partner no proporcionado al componente de cursos.");
        this.state.isLoading = false;
        this.state.error = "No se pudo identificar al usuario.";
        return;
      }
      await this.loadSubscribedCourses();
    });
  }

  /**
   * Asynchronously loads the subscribed courses for the current user via an RPC call.
   * Updates the component's state with the retrieved courses or an error message if the call fails.
   * Additionally, updates the text content of an HTML element to reflect the number of courses loaded.
   *
   * @async
   * @function
   * @throws {Error} If the RPC call fails, an error message is logged, and the state is updated with an error message.
   */
  async loadSubscribedCourses() {
    this.state.isLoading = true;
    this.state.error = null;
    try {
      // Call to the Python endpoint controller
      const result = await rpc("/my_portal/subscribed_courses", {
        partner_id: this.props.partnerId,
      });
      this.state.courses = result;
      console.log("Cursos cargados:", this.state.courses);
    } catch (err) {
      console.error("Error al cargar los cursos suscritos:", err);
      this.state.error = "Ocurrió un error al cargar tus cursos.";
    } finally {
      this.state.isLoading = false;
      // ❌ Ideally, this logic should be moved to the template for better separation of concerns.
      const h3_it = document.querySelector("h3.h3_portal_courses");
      h3_it.textContent = `Mis Cursos (${this.state.courses.length})`;
    }
  }
}

// Register the component so that <owl-component name="..."> can find it
registry
  .category("public_components")
  .add("elearning_portal.SubscribedCourses", SubscribedCourses);
