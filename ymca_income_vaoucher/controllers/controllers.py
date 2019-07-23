# -*- coding: utf-8 -*-
from odoo import http

# class CustomAddons/ymcaIncomeVaoucher(http.Controller):
#     @http.route('/custom_addons/ymca_income_vaoucher/custom_addons/ymca_income_vaoucher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_addons/ymca_income_vaoucher/custom_addons/ymca_income_vaoucher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_addons/ymca_income_vaoucher.listing', {
#             'root': '/custom_addons/ymca_income_vaoucher/custom_addons/ymca_income_vaoucher',
#             'objects': http.request.env['custom_addons/ymca_income_vaoucher.custom_addons/ymca_income_vaoucher'].search([]),
#         })

#     @http.route('/custom_addons/ymca_income_vaoucher/custom_addons/ymca_income_vaoucher/objects/<model("custom_addons/ymca_income_vaoucher.custom_addons/ymca_income_vaoucher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_addons/ymca_income_vaoucher.object', {
#             'object': obj
#         })