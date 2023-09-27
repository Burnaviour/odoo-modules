# -*- coding: utf-8 -*-
# from odoo import http


# class UpdateContactKknV16(http.Controller):
#     @http.route('/update_contact_kkn_v16/update_contact_kkn_v16', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/update_contact_kkn_v16/update_contact_kkn_v16/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('update_contact_kkn_v16.listing', {
#             'root': '/update_contact_kkn_v16/update_contact_kkn_v16',
#             'objects': http.request.env['update_contact_kkn_v16.update_contact_kkn_v16'].search([]),
#         })

#     @http.route('/update_contact_kkn_v16/update_contact_kkn_v16/objects/<model("update_contact_kkn_v16.update_contact_kkn_v16"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('update_contact_kkn_v16.object', {
#             'object': obj
#         })
