# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kkn_edit_pop_module(models.Model):
    _name = 'edit_pop_module'
    _description = 'edit_pop_module'

    name = fields.Char()