import odoo
import odoo.http as http
from odoo.http import request


class PortalElearningController(http.Controller):
    @http.route("/my_portal/subscribed_courses", type="json", auth="user", website=True)
    def get_subscribed_courses(self, partner_id=None, **kw):
        """
        Endpoint JSON para obtener los cursos a los que está suscrito un partner.
        'auth="user"' asegura que solo usuarios logueados puedan llamar.
        """
        # Verificación básica de seguridad/lógica
        current_user_partner_id = request.env.user.partner_id.id
        # Idealmente, deberías usar el partner_id del usuario logueado,
        # pero si confías en el prop pasado
        # (ya que vino del renderizado inicial del servidor),
        # puedes usar el 'partner_id' recibido. Por seguridad, comparar es mejor:
        if not partner_id or partner_id != current_user_partner_id:
            # Opcionalmente podrías usar current_user_partner_id directamente
            # si no pasas props
            # return self._fetch_courses_for_partner(current_user_partner_id)
            # Por ahora, si no coincide o no viene, devolvemos vacío o error
            # raise UserError("Acceso no autorizado o ID de partner inválido.")
            # O manejarlo más suave
            return []  # Devolver lista vacía si hay discrepancia o falta ID

        return self._fetch_courses_for_partner(partner_id)

    def _fetch_courses_for_partner(self, partner_id):
        """Método auxiliar para buscar los cursos."""
        try:
            # Buscamos las suscripciones del partner en slide.channel.partner
            # Asegúrate de que el usuario del portal tenga derechos
            # de lectura sobre estos modelos
            subscriptions = (
                request.env["slide.channel.partner"]
                .sudo()
                .search([("partner_id", "=", partner_id)])
            )
            # Obtenemos los IDs de los canales (cursos)
            channel_ids = subscriptions.mapped("channel_id").ids

            # Buscamos los detalles de esos canales
            courses = (
                request.env["slide.channel"]
                .sudo()
                .search_read(
                    [("id", "in", channel_ids)],
                    ["id", "name"],  # Añade más campos si los necesitas en el frontend
                )
            )
            return courses
        except Exception as e:
            # Loggear el error real en el servidor es buena idea
            odoo.exceptions.UserError(f"Error fetching subscribed courses: {e}")
            return []  # Devolver vacío en caso de error
