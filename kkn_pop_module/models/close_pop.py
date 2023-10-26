# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_close_pop_module(models.Model):
    _name = 'close_pop_module'
    _description = 'close_pop_module'

    name = fields.Char()
