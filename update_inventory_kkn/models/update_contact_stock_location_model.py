# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied


class add_location(models.Model):
    _inherit = 'stock.location'

    cnic = fields.Char(tracking=True)
    street = fields.Char(tracking=True)
    street2 = fields.Char(tracking=True)
    city_id = fields.Many2one('res.district', tracking=True)
    state_id = fields.Many2one(related='city_id.state_id', tracking=True)
    station_id = fields.Many2one('res.station', "res.district")
    zip_id = fields.Char(related='station_id.zip', tracking=True)
    country_id = fields.Many2one(related='state_id.country_id', tracking=True)
