# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResDistrict(models.Model):
    _name = 'res.district'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Districts'
    name = fields.Char('Name')
    code = fields.Char('City Code')
    region_id = fields.Many2one('res.region', 'Region', required=True, tracking=True)
    state_id = fields.Many2one('res.country.state', 'Province', required=True, tracking=True)


