# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_mobile_module(models.Model):
    _name = 'assign_mobile_module'
    _description = 'assign_mobile_module'

    name = fields.Char()


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class kkn_unassign_mobile_module(models.Model):
    _name = 'unassign_mobile_module'
    _description = 'unassign_mobile_module'

    name = fields.Char()


class kkn_mobile_bills_module(models.Model):
    _name = 'mobile_bills_module'
    _description = 'mobile_bills_module'

    name = fields.Char()


class kkn_mobile_packages_module(models.Model):
    _name = 'mobile_packages_module'
    _description = 'mobile_packages_module'

    name = fields.Char()


class kkn_mobile_numbers_module(models.Model):
    _name = 'mobile_numbers_module'
    _description = 'mobile_numbers_module'

    name = fields.Char()
