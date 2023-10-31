# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_mobile_module(models.Model):
    _name = 'assign.mobile.model'
    _description = 'assign_mobile_model'

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
    _name = 'unassign.mobile.model'
    _description = 'unassign_mobile_model'

    name = fields.Char()


class kkn_mobile_bills_module(models.Model):
    _name = 'mobile.bills.model'
    _description = 'mobile_bills_module'

    name = fields.Char()


class kkn_mobile_packages_module(models.Model):
    _name = 'mobile.packages.model'
    _description = 'mobile_packages_module'

    name = fields.Char()


class kkn_mobile_numbers_module(models.Model):
    _name = 'mobile.numbers.model'
    _description = 'mobile_numbers_module'

    name = fields.Char()
