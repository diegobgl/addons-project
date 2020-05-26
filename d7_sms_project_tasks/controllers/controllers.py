# -*- coding: utf-8 -*-
from odoo import http

# class D7SmsProjectTasks(http.Controller):
#     @http.route('/d7_sms_project_tasks/d7_sms_project_tasks/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/d7_sms_project_tasks/d7_sms_project_tasks/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('d7_sms_project_tasks.listing', {
#             'root': '/d7_sms_project_tasks/d7_sms_project_tasks',
#             'objects': http.request.env['d7_sms_project_tasks.d7_sms_project_tasks'].search([]),
#         })

#     @http.route('/d7_sms_project_tasks/d7_sms_project_tasks/objects/<model("d7_sms_project_tasks.d7_sms_project_tasks"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('d7_sms_project_tasks.object', {
#             'object': obj
#         })