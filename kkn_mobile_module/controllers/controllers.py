# -*- coding: utf-8 -*-
# from odoo import http


# class KknMobileModule(http.Controller):
#     @http.route('/kkn_mobile_module/kkn_mobile_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kkn_mobile_module/kkn_mobile_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kkn_mobile_module.listing', {
#             'root': '/kkn_mobile_module/kkn_mobile_module',
#             'objects': http.request.env['kkn_mobile_module.kkn_mobile_module'].search([]),
#         })

#     @http.route('/kkn_mobile_module/kkn_mobile_module/objects/<model("kkn_mobile_module.kkn_mobile_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kkn_mobile_module.object', {
#             'object': obj
#         })
