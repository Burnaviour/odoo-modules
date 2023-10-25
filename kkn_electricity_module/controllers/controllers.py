# -*- coding: utf-8 -*-
# from odoo import http


# class KknElectricityModule(http.Controller):
#     @http.route('/kkn_electricity_module/kkn_electricity_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kkn_electricity_module/kkn_electricity_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kkn_electricity_module.listing', {
#             'root': '/kkn_electricity_module/kkn_electricity_module',
#             'objects': http.request.env['kkn_electricity_module.kkn_electricity_module'].search([]),
#         })

#     @http.route('/kkn_electricity_module/kkn_electricity_module/objects/<model("kkn_electricity_module.kkn_electricity_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kkn_electricity_module.object', {
#             'object': obj
#         })
