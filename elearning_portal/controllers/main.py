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
        current_user_partner_id = request.env.user.partner_id.id
        # Ideally, you should use the logged-in user's partner_id,
        # but if you trust the passed partner_id
        # (since it came from the server's initial rendering),
        # you can use the received 'partner_id'. For security, comparison is better:
        if not partner_id or partner_id != current_user_partner_id:
            # Optionally, you could use current_user_partner_id directly
            # if you don't pass props
            # return self._fetch_courses_for_partner(current_user_partner_id)
            # For now, if it doesn't match or is missing, return empty or error
            # raise UserError("Unauthorized access or invalid partner ID.")
            # Or handle it more gracefully
            return []  # Return an empty list if there's a mismatch or missing ID

        return self._fetch_courses_for_partner(partner_id)

    def _fetch_courses_for_partner(self, partner_id):
        """Helper method to fetch courses."""
        try:
            # Fetch the partner's subscriptions in slide.channel.partner
            # Ensure the portal user has read rights on these models
            subscriptions = (
                request.env["slide.channel.partner"]
                .sudo()
                .search([("partner_id", "=", partner_id)])
            )
            # Get the IDs of the channels (courses)
            channel_ids = subscriptions.mapped("channel_id").ids

            # Fetch the details of those channels
            courses = (
                request.env["slide.channel"]
                .sudo()
                .search_read(
                    [("id", "in", channel_ids)],
                    ["id", "name"],  # Add more fields if needed in the frontend
                )
            )
            return courses
        except Exception as e:
            # Logging the actual error on the server is a good idea
            odoo.exceptions.UserError(f"Error fetching subscribed courses: {e}")
            return []  # Return empty in case of error
