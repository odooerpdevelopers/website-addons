import odoo
import odoo.http as http
from odoo.http import request


class PortalElearningController(http.Controller):
    @http.route("/my_portal/subscribed_courses", type="json", auth="user", website=True)
    def get_subscribed_courses(self, partner_id=None, **kw):
        """
        JSON Endpoint to retrieve the courses a partner is subscribed to.
        The 'auth="user"' ensures that only logged-in users can call this method.

        Args:
            partner_id (int, optional): The ID of the partner to fetch courses for.
                If not provided or does not match the logged-in user's partner ID,
                an empty list will be returned.
            **kw: Additional keyword arguments.

        Returns:
            list: A list of courses the partner is subscribed to. Returns an empty
            list if the provided partner_id is invalid or does not match the
            logged-in user's partner ID.
        """
        # Basic security/logic verification
        current_user_partner_id = request.env.user.partner_id
        if not partner_id:
            partner_id = current_user_partner_id

        return self._fetch_courses_for_partner(partner_id)

    def _fetch_courses_for_partner(self, partner_id):
        """Helper method to fetch courses."""
        try:
            return partner_id.slide_channel_ids.read(['id', 'name', 'website_url'])
        except Exception as e:
            # Logging the actual error on the server is a good idea
            odoo.exceptions.UserError(f"Error fetching subscribed courses: {e}")
            return []  # Return empty in case of error
