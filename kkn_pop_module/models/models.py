# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied, ValidationError
import datetime
from dateutil.relativedelta import relativedelta

AVAILABLE_PRIORITIES = [
    ("0", "Low"),
    ("1", "Medium"),
    ("2", "High"),
    ("3", "Very High"),
]


class kkn_pop_module(models.Model):
    _name = 'add.pop.model'
    _description = 'Add POP'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    color = fields.Integer("Color Index")
    kanban_state = fields.Selection(
        [("normal", "Grey"), ("done", "Green"), ("blocked", "Red")],
        string="Kanban State",
        copy=False,
        default="normal",
        required=True,
    )
    priority = fields.Selection(
        AVAILABLE_PRIORITIES,
        string="Priority",
        index=True,
        default=AVAILABLE_PRIORITIES[0][0],
    )

    state = fields.Selection(
        [
            ("New", "New"),
            ("Approval Required", "Admin Approval"),
            ("COO Approval", "COO Approval"),
            ("CEO Approval", "CEO Approval"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected"),
            ("Closed", "Closed"),
        ],
        string="State",
        group_expand="_expand_states",
        readonly=True,
        index=True,
        copy=False,
        default="New",
        tracking=True,
    )

    pop_new_type = fields.Selection(
        [
            ("New", "New POP"),
            ("Existing", "Existing POP"),
        ],
        string="POP Type",
        default="New",
    )
    is_rental = fields.Selection(
        [
            ("Yes", "Yes"),
            ("No", "No"),
        ],
        string="Is Rental",
        default="Yes",
    )
    existing_location_id = fields.Many2one(
        "stock.location",
        "Existing Location",
        domain="[('usage', 'in', ('customer', 'costcenter'))]",
    )

    @api.onchange("pop_new_type")
    def _onchange_pop_location_new(self):
        self.is_rental = "Yes"

    @api.onchange("existing_location_id", "pop_new_type")
    def _onchange_existing_location(self):
        self.name = False
        self.location_id = self.env["stock.location"].search([("name", "=", "KKN")]).id
        self.usage = "pop"
        self.street = self.existing_location_id.street
        self.city_id = self.env["res.district"].search([("code", "=", "LHR")]).id
        self.state_id = (
            self.env["res.country.state"].search([("code", "=", "PK-PJ")]).id
        )
        self.country_id = self.env["res.country"].search([("name", "=", "PAKISTAN")]).id
        self.zip_id = 54000
        self.partner_latitude = 0.00000
        self.partner_longitude = 0.00000

        if self.pop_new_type == "Existing":
            if self.existing_location_id:
                self.usage = self.existing_location_id.usage
                self.street = self.existing_location_id.street
                self.name = self.existing_location_id.name
                self.location_id = self.existing_location_id.location_id
                self.city_id = self.existing_location_id.city_id
                self.state_id = self.existing_location_id.state_id
                self.country_id = self.existing_location_id.country_id
                self.zip_id = self.existing_location_id.zip_id
                self.partner_latitude = self.existing_location_id.partner_latitude
                self.partner_longitude = self.existing_location_id.partner_longitude
        else:
            self.existing_location_id = False

    name = fields.Char("Location Name", tracking=True)
    complete_name = fields.Char("Full Location Name", store=True, tracking=True)
    location_id = fields.Many2one(
        "stock.location",
        "Parent Location",
        index=True,
        ondelete="cascade",
        check_company=True,
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.",
        tracking=True,
        default=lambda self: self.env["stock.location"]
        .search([("name", "=", "KKN")])
        .id,
    )
    cost_center_id = fields.Many2one("account.analytic.account", "Cost Center")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        help='Let this field empty if this location is shared between companies')
    city_code = fields.Char(related='city_id.code', tracking=True)

    # Unique ID for location form
    unique_id = fields.Char(string="Unique ID", tracking=True)

    file_upload = fields.Binary(string="Documents", tracking=True)
    file_name = fields.Char(tracking=True, string="Rental Agreement")

    # New Type in usage Pop
    usage = fields.Selection(
        related="created_location.usage", string="Location Type", tracking=True
    )
    partner_latitude = fields.Float("Geo Latitude", digits=(16, 6), tracking=True)
    partner_longitude = fields.Float("Geo Longitude", digits=(16, 6), tracking=True)
    date_localization = fields.Date(string="Geolocation Date", tracking=True)
    comment = fields.Text("Additional Information")

    street = fields.Char(tracking=True, required=True)
    street2 = fields.Char(tracking=True)
    city_id = fields.Many2one(
        "res.district",
        tracking=True,
        default=lambda self: self.env["res.district"].search([("code", "=", "LHR")]).id,
        required=True,
    )
    state_id = fields.Many2one(
        "res.country.state",
        tracking=True,
        default=lambda self: self.env["res.country.state"]
        .search([("code", "=", "PK-PJ")])
        .id,
        required=True,
    )
    zip_id = fields.Char(tracking=True, default="54000")
    country_id = fields.Many2one(
        "res.country",
        domain="[('name','=','PAKISTAN')]",
        tracking=True,
        default=lambda self: self.env["res.country"]
        .search([("name", "=", "PAKISTAN")])
        .id,
        required=True,
    )

    landlord_name = fields.Many2one(
        "res.partner", string="Landlord Name", tracking=True
    )
    landlord_cnic = fields.Char(
        related="landlord_name.cnic", string="Landlord CNIC", tracking=True
    )
    landlord_mobile = fields.Char(
        related="landlord_name.mobile", string="Landlord Mobile", tracking=True
    )
    landlord_email = fields.Char(
        related="landlord_name.email",
        string="Landlord Email",
        tracking=True,
        required=False,
    )
    rent = fields.Monetary(
        string="Agreement Rent", currency_field="company_currency", tracking=True
    )
    security = fields.Monetary(
        string="Security", currency_field="company_currency", tracking=True
    )
    company_currency = fields.Many2one(
        string="Currency",
        related="company_id.currency_id",
        readonly=True,
        relation="res.currency",
    )

    time_period = fields.Char(string="Lease Term Year(s)", tracking=True)
    time_period_unit = fields.Many2one(
        "uom.uom",
        string="Lease Term Unit",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "Year(s)")]).id,
        tracking=True,
    )
    agreement_date = fields.Date(string="Agreement Date", tracking=True)
    annual_increment = fields.Integer(string="Annual Increment (%)", tracking=True)
    payment_terms = fields.Selection(
        [
            ("monthly", "monthly"),
            ("quarterly", "quarterly"),
            ("by annually", "by annually"),
            ("annually", "annually"),
        ],
        string="Payment Terms",
        tracking=True,
    )

    payment_mode = fields.Selection(
        [
            ("Cash", "Cash"),
            ("Bank", "Bank"),
        ],
        string="Payment Mode",
        tracking=True,
    )
    bank_name = fields.Char("Bank Name", tracking=True)
    account_no = fields.Char("Account No", tracking=True)
    account_title = fields.Char("Account Title", tracking=True)
    tax_ids = fields.Many2many("account.tax")
    company_type = fields.Selection(
        string="Company Type",
        selection=[("person", "Individual"), ("company", "Company")],
        tracking=True,
        default="person",
    )

    vat = fields.Char(
        string="NTN",
        index=True,
        help="The Tax Identification Number. "
        "Complete it if the contact is subjected to government taxes. "
        "Used in some legal statements.",
    )
    partner_id = fields.Many2one("res.partner", "Vendor", tracking=True)
    next_billing_date = fields.Date("Next Billing Date", tracking=True)
    no_of_years = fields.Integer("No of Years")
    utility_status = fields.Selection(
        [("Included", "Included"), ("Not Included", "Not Included")],
        string="Utility Status",
        tracking=True,
    )
    meter_num = fields.Char(string="Meter Number", tracking=True)
    billing_date = fields.Date(string="Billing Date", tracking=True)

    room_loc = fields.Char(string="Room Location", tracking=True)
    room_size = fields.Integer(string="Room Size", tracking=True)
    room_size_unit = fields.Many2one(
        "uom.uom",
        string="Lease Term Unit",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "Sq(FT)")]).id,
        tracking=True,
    )
    roof_size = fields.Integer(string="Roof Size", tracking=True)
    roof_size_unit = fields.Many2one(
        "uom.uom",
        string="Lease Term Unit",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "Sq(FT)")]).id,
        tracking=True,
    )
    access_status = fields.Boolean(string="Access Status")

    tower_installed = fields.Selection(
        [("Yes", "Yes"), ("No", "No")], string="Tower Installed", tracking=True
    )
    tower_height = fields.Integer(string="Tower Height", tracking=True)

    rent_line = fields.One2many("add.pop.rent.bill", "name")
    service_line = fields.One2many("add.pop.service.bill", "name")
    generator_line = fields.One2many("add.pop.generator.bill", "name")
    electricity_rent_line = fields.One2many("add.pop.rent.bill", "name1")
    next_amount_paid = fields.Monetary(
        string="Current Rent", currency_field="company_currency", tracking=True
    )

    rent_electricity_bill_due = fields.Date(
        string="Electricity Billing Due Date", tracking=True
    )
    rent_electricity_amount = fields.Monetary(
        string="Electricity Billing Amount",
        currency_field="company_currency",
        tracking=True,
    )
    created_location = fields.Many2one("stock.location", "Location")
    is_service_charges = fields.Boolean(string="Service Charges")
    is_generator_charges = fields.Boolean(string="Generator Charges")
    service_charges = fields.Monetary(
        string="Service Charges Amount",
        currency_field="company_currency",
        tracking=True,
    )
    generator_charges = fields.Monetary(
        string="Generator Charges Amount",
        currency_field="company_currency",
        tracking=True,
    )

    @api.model
    def _geo_localize(self, street="", zip="", city="", state="", country=""):
        geo_obj = self.env["base.geocoder"]
        search = geo_obj.geo_query_address(
            street=street, zip=zip, city=city, state=state, country=country
        )
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    # Get address along city, state adn country and write latitude, longitude
    def geo_localize_location(self):
        # We need country names in English below
        for partner in self.with_context(lang="en_US"):
            if result := self._geo_localize(
                partner.street,
                partner.zip_id,
                partner.city_id.name,
                partner.state_id.name,
                partner.country_id.name,
            ):
                partner.write(
                    {
                        "partner_latitude": result[0],
                        "partner_longitude": result[1],
                        "date_localization": fields.Date.context_today(partner),
                    }
                )
        return True


class noc_wireless_report(models.Model):
    _name = "stock.location.pop.report"

    type_of = fields.Selection(
        [("all", "All"), ("custom", "Custom")],
        required=True,
        default="custom",
        string="Type",
    )
    location_id = fields.Many2many(
        "stock.location",
        string="Location",
        domain="['|',('usage', '=', 'pop')," "('customer_is_pop', '=', True)]",
    )

    @api.onchange("type_of")
    def _onchange_type_of(self):
        self.location_id = False

    # def print_report(self):
    #     domains = []
    #     if self.type_of == "custom":
    #         domains.append(("id", "in", self.location_id.ids))
    #     else:
    #         domains.append("|")
    #         domains.append(("usage", "=", "pop"))
    #         domains.append(("customer_is_pop", "=", True))
    #     data = {"domains": domains}
    #     return self.env.ref(
    #         "add.pop.module.stock_location_pop_report_id"
    #     ).report_action(self, data=data)



class RentBillsHistory(models.Model):
    _name = "add.pop.rent.bill"
    _description = "POP RENT BILL HISTORY"
    name = fields.Many2one("add.pop.module")
    name1 = fields.Many2one("add.pop.module")
    move_id = fields.Many2one("account.move")
    billing_date = fields.Date("Billing Date")



class ServiceBillsHistory(models.Model):
    _name = "add.pop.service.bill"
    _description = "POP SERVICE BILL HISTORY"
    name = fields.Many2one("add.pop.module")
    move_id = fields.Many2one("account.move")
    billing_date = fields.Date("Billing Date")



class GeneratorBillsHistory(models.Model):
    _name = "add.pop.generator.bill"
    _description = "POP GENERATOR BILL HISTORY"
    name = fields.Many2one("add.pop.module")
    move_id = fields.Many2one("account.move")
    billing_date = fields.Date("Billing Date")
