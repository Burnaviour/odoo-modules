# -*- coding: utf-8 -*-
# from odoo import http


# class UpdateCrmKkn(http.Controller):
#     @http.route('/update_crm_kkn/update_crm_kkn', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/update_crm_kkn/update_crm_kkn/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('update_crm_kkn.listing', {
#             'root': '/update_crm_kkn/update_crm_kkn',
#             'objects': http.request.env['update_crm_kkn.update_crm_kkn'].search([]),
#         })

#     @http.route('/update_crm_kkn/update_crm_kkn/objects/<model("update_crm_kkn.update_crm_kkn"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('update_crm_kkn.object', {
#             'object': obj
#         })
