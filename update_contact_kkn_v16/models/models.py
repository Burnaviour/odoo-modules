# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    unique_id = fields.Char(
        string="unique_id",
        default=lambda self: _("New"),
        readonly=True,
        required=True,
    )

    @api.model
    def create(self, values):
        """
        Overrides the create method of the base model class to generate a unique ID based on the company type when creating a new partner.

        :param values: Dictionary containing the data for the new partner record.
        :return: The ID of the new partner record.
        """
        id_type = values.get("company_type")

        if values.get("unique_id", _("New")) == _("New"):
            if id_type == "person":
                values["unique_id"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.residential"
                ) or _("New")
            elif id_type == "company":
                values["unique_id"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.company"
                ) or _("New")
            else:
                values["unique_id"] = "N/A"
            result = super().create(values)

        return result

    def generate_id(self, company):
        """
        Generates a unique ID based on the company type.

        :param company: The company type.
        """

        if company == "person":
            sequence = "res.partner.residential"
        elif company == "company":
            sequence = "res.partner.company"
        else:
            sequence = False
        if sequence:
            self.unique_id = self.env["ir.sequence"].next_by_code(sequence)

    def write(self, vals):
        """
        Overrides the write method of the base model class to update the unique ID when the company type is changed.

        :param vals: Dictionary containing the values to be updated.
        :return: The result of the write operation.
        """
        if "company_type" in vals:
            if self.company_type != vals["company_type"]:
                self.generate_id(vals["company_type"])
        return super().write(vals)
