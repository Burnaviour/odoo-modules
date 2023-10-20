# -*- coding: utf-8 -*-
# from odoo import http


# class KknPopModule(http.Controller):
#     @http.route('/kkn_pop_module/kkn_pop_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kkn_pop_module/kkn_pop_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kkn_pop_module.listing', {
#             'root': '/kkn_pop_module/kkn_pop_module',
#             'objects': http.request.env['kkn_pop_module.kkn_pop_module'].search([]),
#         })

#     @http.route('/kkn_pop_module/kkn_pop_module/objects/<model("kkn_pop_module.kkn_pop_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kkn_pop_module.object', {
#             'object': obj
#         })
