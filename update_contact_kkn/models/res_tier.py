# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResTier(models.Model):
    _name = 'res.tier'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, tracking=True)