# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class update_inventory_kkn(models.Model):
#     _name = 'update_inventory_kkn.update_inventory_kkn'
#     _description = 'update_inventory_kkn.update_inventory_kkn'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
