# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResStation(models.Model):
    _name = 'res.station'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Stations'

    name = fields.Char('Name', required=True, tracking=True)
    district_id = fields.Many2one('res.district', 'District', required=True, tracking=True)
    tier_id = fields.Many2one('res.tier', string='Tier', tracking=True)
    region_id = fields.Many2one(related='district_id.region_id', store=True, tracking=True)
    state_id = fields.Many2one(related='district_id.state_id', store=True, tracking=True)
    zip = fields.Char('Zip Code', tracking=True)