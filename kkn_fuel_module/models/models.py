# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_fuel_module(models.Model):
    _name = 'kkn_fuel_module.kkn_fuel_module'
    _description = 'kkn_fuel_module.kkn_fuel_module'
    name = fields.Char()
