# -*- coding: utf-8 -*-
# from odoo import http


# class UpdateInventoryKkn(http.Controller):
#     @http.route('/update_inventory_kkn/update_inventory_kkn', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/update_inventory_kkn/update_inventory_kkn/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('update_inventory_kkn.listing', {
#             'root': '/update_inventory_kkn/update_inventory_kkn',
#             'objects': http.request.env['update_inventory_kkn.update_inventory_kkn'].search([]),
#         })

#     @http.route('/update_inventory_kkn/update_inventory_kkn/objects/<model("update_inventory_kkn.update_inventory_kkn"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('update_inventory_kkn.object', {
#             'object': obj
#         })
