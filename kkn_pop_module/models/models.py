# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_pop_module(models.Model):
    _name = 'add_pop_module'
    _description = 'add_pop_module'

    name = fields.Char()


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class kkn_edit_pop_module(models.Model):
    _name = 'edit_pop_module'
    _description = 'edit_pop_module'

    name = fields.Char()


class kkn_close_pop_module(models.Model):
    _name = 'close_pop_module'
    _description = 'close_pop_module'

    name = fields.Char()
