# -*- coding: utf-8 -*-
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


ADDRESS_FIELDS = ("street", "street2", "zip", "city", "state_id", "country_id")


class ResPartner(models.Model):
    _inherit = "res.partner"

    contact_type = fields.Selection(
        [
            ("customer", "CUSTOMER"),
            ("vendor", "VENDOR"),
            ("employee", "Employee"),
            ("installation_poc", "Installation POC"),
            ("billing_poc", "Billing POC"),
            ("portal", "Portal User"),
            ("other", "OTHERS"),
        ],
        string="Contact Type",
        required=True,
        tracking=True,
    )
    contact_sub_type = fields.Selection(
        [
            ("residential", "RESIDENTIAL"),
            ("small_business", "SMALL BUSINESS"),
            ("corporate", "CORPORATE"),
            ("carriers_operators", "CARRIERS & OPERATORS"),
        ],
        string="Contact Sub Type",
        default=False,
        tracking=True,
    )

    customer_subscription_model = fields.Selection(
        [("pre_paid", "Pre Paid"), ("post_paid", "Post Paid")],
        string="Subscription Model",
    )

    # unique_id = fields.Char(string="Unique ID", tracking=True, store=True)
    unique_id = fields.Char(
        string="unique_id",
        default=lambda self: _("New"),
        readonly=True,
        required=True,
        tracking=True,
    )

    pta_registered = fields.Selection(
        [("registered", "Registered"), ("unregistered", "Unregistered")],
        string="PTA Registered",
        tracking=True,
    )
    vat = fields.Char(
        string="Tax ID",
        index=True,
        help="The Tax Identification Number. Complete it if the contact is subjected "
        "to government taxes. Used in some legal statements.",
        tracking=True,
    )
    gstn = fields.Char(string="GSTN", tracking=True)

    # reseller = fields.Selection(
    #     [("yes", "Yes"), ("no", "No")], string="Reseller", required=False, tracking=True
    # )

    tax_status = fields.Selection(
        [("registered", "Registered"), ("unregistered", "Unregistered")],
        string="Tax Status",
        default="unregistered",
        tracking=True,
    )
    cnic = fields.Char(string="CNIC")
    district_id = fields.Many2one("res.district", "District", tracking=True)
    station_id = fields.Many2one("res.station", "Station", tracking=True)
    zip = fields.Char(
        related="station_id.zip", change_default=True, store=True, tracking=True
    )
    state_id = fields.Many2one(
        related="district_id.state_id", store=True, tracking=True
    )
    country_id = fields.Many2one(
        related="state_id.country_id", store=True, tracking=True
    )

    start_date = fields.Date(string="Starting Date", default=fields.Date.context_today)
    status = fields.Boolean(string="Status", default=True)

    @api.onchange("district_id")
    def _onchange_district(self):
        self.station_id = False

    @api.onchange("cnic")
    def _onchange_cnic(self):
        if self.cnic:
            search_cnic = self.env["res.partner"].search_count(
                [("cnic", "=", self.cnic), ("id", "not in", self.ids)]
            )
            if search_cnic > 0:
                raise ValidationError(_("CNIC No Already Exist"))

    @api.onchange("tax_status")
    def onchange_tax_status(self):
        if self.tax_status:  # == 'unregistered':
            self.pta_registered = False

    @api.model
    def create(self, vals_list):
        """
        Overrides the create method of the base model class to generate a unique ID based on the company type when creating a new partner.

        :param values: Dictionary containing the data for the new partner record.
        :return: The ID of the new partner record.
        """
        if vals_list.get("unique_id", _("New")) == _("New"):
            id_type = vals_list.get("company_type")
            contact_type = vals_list.get("contact_type")
            contact_sub_type = vals_list.get("contact_sub_type")
            _logger.error(
                "%s      %s        %s  ", id_type, contact_type, contact_sub_type
            )
            vals_list["unique_id"] = self._generate_unique_id(
                id_type, contact_type, contact_sub_type
            )
        return super().create(vals_list)

    def _generate_unique_id(self, id_type, contact_type, contact_sub_type):
        """
        Generates a unique ID based on the input values.

        :param id_type: The type of the partner (person or company).
        :type id_type: str
        :param contact_type: The type of contact (customer, vendor, employee, etc.).
        :type contact_type: str
        :param contact_sub_type: The sub-type of contact (residential, small_business, corporate, etc.).
        :type contact_sub_type: str
        :return: The generated unique ID.
        :rtype: str
        """
        unique_id_sequence_mapping = {
            ("person", "customer", "residential"): "res.partner.residential",
            ("person", "customer", "small_business"): "res.partner.small.business",
            ("person", "customer", "corporate"): "res.partner.corporate",
            (
                "person",
                "customer",
                "carriers_operators",
            ): "res.partner.carriers.operators",
            ("person", "vendor", False): "res.partner.vendor",
            ("person", "employee", False): "res.partner.employee",
            ("person", "other", False): "res.partner.other",
            ("person", "installation_poc", False): "res.partner.installation.poc",
            ("person", "billing_poc", False): "res.partner.billing.poc",
            ("person", "portal", False): "res.partner.portal.user",
            ("company", "customer", "residential"): "res.partner.comp.residential",
            (
                "company",
                "customer",
                "small_business",
            ): "res.partner.comp.small.business",
            ("company", "customer", "corporate"): "res.partner.comp.corporate",
            (
                "company",
                "customer",
                "carriers_operators",
            ): "res.partner.comp.carriers.operators",
            ("company", "vendor", False): "res.partner.comp.vendor",
            ("company", "employee", False): "res.partner.comp.employee",
            ("company", "other", False): "res.partner.comp.other",
            ("company", "installation_poc", False): "res.partner.comp.installation.poc",
            ("company", "billing_poc", False): "res.partner.comp.billing.poc",
            ("company", "portal", False): "res.partner.comp.portal.user",
            ("company", False, False): "res.partner.company",
        }

        if sequence := unique_id_sequence_mapping.get(
            (id_type, contact_type, contact_sub_type)
        ):
            return self.env["ir.sequence"].next_by_code(sequence) or _("New")
        return "N/A"

    @api.model
    def write(self, vals):
        """
        Overrides the write method of the base model class to update the unique ID when the company type is changed.

        :param vals: Dictionary containing the values to be updated.
        :return: The result of the write operation.
        """

        if any(
            field in vals
            for field in ["company_type", "contact_type", "contact_sub_type"]
        ):
            id_type = vals.get("company_type", self.company_type)
            contact_type = vals.get("contact_type", self.contact_type)
            contact_sub_type = vals.get("contact_sub_type", self.contact_sub_type)

            # logger for debugging

            # _logger.error(
            #     "%s   %s     %s  ", contact_type, contact_sub_type, id_type
            # )

            if contact_type != "customer":
                vals["contact_sub_type"] = ""
                contact_sub_type = False

            vals["unique_id"] = self._generate_unique_id(
                id_type, contact_type, contact_sub_type
            )
        return super().write(vals)
