from odoo import http
from odoo.http import request
import json


class AddPartnerController(http.Controller):

    @http.route('/add-partner/', type='http', auth='public', website=True, csrf=False)
    def add_partner(self, **post):

        partner_vals = {
            'name': post.get('name'),
            'email': post.get('email')
        }
        partner_id = request.env['res.partner'].sudo().create(partner_vals)
        return request.redirect('/contactus-thank-you')
