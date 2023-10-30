# -*- coding: utf-8 -*-

from odoo import models, fields, api


class updateLocationForm(models.Model):
    _name = 'stock.location'
    _inherit = ['stock.location', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Location Name', required=True, tracking=True)
    complete_name = fields.Char("Full Location Name", compute='_compute_complete_name', store=True, tracking=True)
    location_id = fields.Many2one(
        'stock.location', 'Parent Location', index=True, ondelete='cascade', check_company=True,
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent "
             "location.",
        tracking=True)

    city_code = fields.Char(related='city_id.code', tracking=True, readonly=True)

    city_id = fields.Many2one('res.district')
    # Unique ID for location form
    unique_id = fields.Char(string='Unique ID', tracking=True, required=True, readonly=True)
    customer_is_pop = fields.Boolean('Is POP?')

    # New Type in usage Pop
    usage = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('pop', 'POP'),
        ('exchange', 'Exchange'),
        ('storeconsumed', 'Store Consumed'),
        ('inventory', 'Inventory Loss'),
        ('production', 'Production'),
        ('costcenter', 'Cost Center'),
        ('transit', 'Transit Location')], string='Location Type',
        default='internal', index=True, required=True,
        help="* Vendor Location: Virtual location representing the source location for products coming from your vendors"
             "\n* View: Virtual location used to create a hierarchical structures for your warehouse, aggregating its child locations ; can't directly contain products"
             "\n* Internal Location: Physical locations inside your own warehouses,"
             "\n* Customer Location: Virtual location representing the destination location for products sent to your customers"
             "\n* Inventory Loss: Virtual location serving as counterpart for inventory operations used to correct stock levels (Physical inventories)"
             "\n* Production: Virtual counterpart location for production operations: this location consumes the components and produces finished products"
             "\n* Transit Location: Counterpart location that should be used in inter-company or inter-warehouses operations",
        tracking=True)
    partner_latitude = fields.Float('Geo Latitude', digits=(16, 6), tracking=True)
    partner_longitude = fields.Float('Geo Longitude', digits=(16, 6), tracking=True)
    date_localization = fields.Date(string='Geolocation Date', tracking=True)

    @api.onchange('city_code')
    def _onchange_city_code(self):
        print('reached')
        if self.city_code:
            sql = "select Max(unique_id) maxcode from stock_location WHERE unique_id LIKE '%" + self.city_code + "%'"
            self.env.cr.execute(sql)
            max_code = self.env.cr.fetchone()
            temp = max_code[0]
            if temp == None:
                self.unique_id = self.city_code + '-1501'
            else:
                if max_code[0] is not None:
                    levelstr5 = str(int(temp[-4:]) + 1)
                    result = self.city_code + '-' + levelstr5
                    self.unique_id = result
        else:
            self.unique_id = False

    # Find Location of given Data
    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    # Get address along city, state adn country and write latitude, longitude
    def geo_localize_location(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize(partner.street,
                                        partner.zip_id,
                                        partner.city_id.name,
                                        partner.state_id.name,
                                        partner.country_id.name)

            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
        return True
