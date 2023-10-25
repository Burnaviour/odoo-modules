# -*- coding: utf-8 -*-
# from odoo import http


# class KknFuelModule(http.Controller):
#     @http.route('/kkn_fuel_module/kkn_fuel_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kkn_fuel_module/kkn_fuel_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kkn_fuel_module.listing', {
#             'root': '/kkn_fuel_module/kkn_fuel_module',
#             'objects': http.request.env['kkn_fuel_module.kkn_fuel_module'].search([]),
#         })

#     @http.route('/kkn_fuel_module/kkn_fuel_module/objects/<model("kkn_fuel_module.kkn_fuel_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kkn_fuel_module.object', {
#             'object': obj
#         })
