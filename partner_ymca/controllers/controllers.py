# -*- coding: utf-8 -*-
from odoo import http

# class CustomAddons/partnerYmca(http.Controller):
#     @http.route('/custom_addons/partner_ymca/custom_addons/partner_ymca/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_addons/partner_ymca/custom_addons/partner_ymca/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_addons/partner_ymca.listing', {
#             'root': '/custom_addons/partner_ymca/custom_addons/partner_ymca',
#             'objects': http.request.env['custom_addons/partner_ymca.custom_addons/partner_ymca'].search([]),
#         })

#     @http.route('/custom_addons/partner_ymca/custom_addons/partner_ymca/objects/<model("custom_addons/partner_ymca.custom_addons/partner_ymca"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_addons/partner_ymca.object', {
#             'object': obj
#         })