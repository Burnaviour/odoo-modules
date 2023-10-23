# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_electricity_module(models.Model):
    _name = 'kkn_electricity_module.kkn_electricity_module'
    _description = 'kkn_electricity_module.kkn_electricity_module'

    name = fields.Char()


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class kkn_bills_electricity_module(models.Model):
    _name = 'kkn_electricity_module.kkn_bills_electricity_module'
    _description = 'kkn_electricity_module.kkn_bills_electricity_module'

    name = fields.Char()


class kkn_electricity_meters_module(models.Model):
    _name = 'kkn_electricity_module.kkn_electricity_meters_module'
    _description = 'kkn_electricity_module.kkn_electricity_meters_module'

    name = fields.Char()
