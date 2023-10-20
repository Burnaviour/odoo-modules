# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    # rec name which is on the top of the bread crumb view
    _rec_name = "name"
    _order = "id desc"
    name = fields.Char(string="Appointment ID")
    patient_id = fields.Many2one("hospital.patients", string="Patients")
    doctor_id = fields.Many2one("res.users", string="Doctors", tracking=True)
    gender = fields.Selection(related="patient_id.gender")
    appointment_time = fields.Datetime(
        string="Appointment Time ", default=fields.Datetime.now
    )
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection(
        [("0", "Very Low"), ("1", "Low"), ("2", "Normal"), ("3", "High")],
        string="Priority",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_consultation", "In Consultation"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
    )
    hide_price = fields.Boolean(string="Hide Sales Price", default=True)

    pharmacy_line_ids = fields.One2many(
        "appointment.pharmacy.lines", "appointment_id", string="Pharmacy Lines"
    )
    operation = fields.Many2one("hospital.operations", string="Operations")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="currency",
        related="company_id.currency_id",
    )

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def unlink(self):
        if self.state == "done":
            raise ValidationError("You cannot delete a record in done state")
        return super(HospitalAppointment, self).unlink()

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_in_consultation(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    # cancel using object call in xml
    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    # cancel using wizard
    # def action_cancel(self):
    #     action = self.env.ref('hospital.action_cancel_appointment').read()[0]
    #     return action

    def reset_to_draft(self):
        for rec in self:
            rec.state = "draft"

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code("hospital.appointment")
        return super(HospitalAppointment, self).create(vals)

    # method triggered when click on save the record
    def write(self, vals_list):
        _logger.error("Hospital %s,%s", vals_list, self)
        if not self.name:
            vals_list["name"] = self.env["ir.sequence"].next_by_code(
                "hospital.appointment"
            )

        return super(HospitalAppointment, self).write(vals_list)

    def test_obj(self):
        _logger.error("%s", self.env.context)
        # obj = self.env["appointment.pharmacy.lines"]
        # self.create(
        #     {
        #         "patient_id": 1,
        #         "pharmacy_line_ids": [
        #             (
        #                 0,
        #                 0,
        #                 {
        #                     "product_id": 1,
        #                 },
        #             )
        #         ],
        #     }
        # )
        # sourcery skip: no-loop-in-tests
        for line in self.pharmacy_line_ids:
            _logger.error("%s", line)
            line.write({'product_id':2})
        # phm_id = obj.create({"appointment_id": self.ids[0], "product_id": 1})
        # _logger.error("%s its here", phm_id)
        return True


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"
    product_id = fields.Many2one("product.product", required=True)
    price_unit = fields.Float(string="Price", related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")

    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="currency",
        related="appointment_id.currency_id",
    )
    price_subtotal = fields.Monetary(
        "Subtotal", compute="_compute_sub_total", currency_field="company_currency_id"
    )

    @api.depends("price_unit", "qty")
    def _compute_sub_total(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty

    @api.model
    def create(self, vals):
        _logger.error(f" Lines create{vals},{self}")
        return super().create(vals)

    def write(self, vals):
        _logger.error(f" Lines write {vals},{self}")
        return super().write(vals)
