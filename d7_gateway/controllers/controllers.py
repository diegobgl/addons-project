# -*- coding: utf-8 -*-
from odoo import http

# class D7Gateway(http.Controller):
#     @http.route('/d7_gateway/d7_gateway/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/d7_gateway/d7_gateway/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('d7_gateway.listing', {
#             'root': '/d7_gateway/d7_gateway',
#             'objects': http.request.env['d7_gateway.d7_gateway'].search([]),
#         })

#     @http.route('/d7_gateway/d7_gateway/objects/<model("d7_gateway.d7_gateway"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('d7_gateway.object', {
#             'object': obj
#         })