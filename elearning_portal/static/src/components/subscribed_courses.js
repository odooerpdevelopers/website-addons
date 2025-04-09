import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

console.log(" elearning_portal: subscribed_courses.js cargado");

export class SubscribedCourses extends Component {
  static template = "elearning_portal.SubscribedCoursesTemplate"; // Nombre de la plantilla XML

  // Props que esperamos recibir desde el QWeb del servidor
  static props = {
    partnerId: { type: [Number, Boolean] }, // Puede ser el ID o False si no hay usuario/partner
  };

  setup() {
    // Hook para llamadas RPC
    console.log("elearning_portal: subscribed_courses.js setup");

    // Estado para almacenar los cursos y el estado de carga
    this.state = useState({
      courses: [],
      isLoading: true,
      error: null,
    });

    // Hook que se ejecuta antes del primer renderizado
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

  showMe(event) {
    alert("Li Clicked")
  }

  // Method para cargar los cursos vía RPC
  async loadSubscribedCourses() {
    this.state.isLoading = true;
    this.state.error = null;
    try {
      // Llamada al endpoint Python que crearemos
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
      const h3_it = document.querySelector("h3.h3_portal_courses");
      h3_it.textContent = `Mis Cursos (${this.state.courses.length})`;
    }
  }
}

// Registramos el componente para que <owl-component name="..."> pueda encontrarlo
registry
  .category("public_components")
  .add("elearning_portal.SubscribedCourses", SubscribedCourses);
