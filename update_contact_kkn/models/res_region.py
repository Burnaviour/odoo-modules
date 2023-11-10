# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResRegion(models.Model):
    _name = 'res.region'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Regions'

    name = fields.Char('Name', required=True, tracking=True)