from odoo import http
# from odoo.http import request

class OwlEventsController(http.Controller):
    @http.route('/owl_events', type='http', auth="public", website=True)
    def owl_events_page(self, **kw):
        return http.request.render('owl_events.owl_events_page')
