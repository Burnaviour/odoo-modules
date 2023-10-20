# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = "hospital.patients"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patients"
    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="Reference")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        search="_search_age",
        inverse="_inverse_dob_cal",
    )
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    description = fields.Text()
    image = fields.Image(string="Image")
    active = fields.Boolean(default=True, string="Active")
    patient_tag = fields.Many2many("patient.tag", string="Tags")
    appointment_count = fields.Integer(
        string="Appointment Count", compute="_compute_appointment_count", store=True
    )
    appointment_ids = fields.One2many(
        "hospital.appointment", "patient_id", string="Appointment"
    )

    def action_view_appointment(self):
        return {
            "name": _("Appointment"),
            "type": "ir.actions.act_window",
            "view_type": "list,form",
            "view_mode": "tree,form",
            "target": "current",
            "res_model": "hospital.appointment",
            "context": {"default_patient_id": self.id},
            "domain": [("patient_id", "=", self.id)],
        }

    @api.depends("dob")
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = fields.Date.today()
                if record.dob:
                    age = today.year - record.dob.year
                    record.age = age
            else:
                record.age = 1  # Default age if dob is not set

    @api.depends("age")
    def _inverse_dob_cal(self):
        for record in self:
            if record.age:
                today = fields.Date.today()
                record.dob = today - relativedelta(years=record.age)

    @api.depends("appointment_ids")
    def _compute_appointment_count(self):
        appointment_group = self.env["hospital.appointment"].read_group(
            domain=[], fields=["patient_id"], groupby=["patient_id"]
        )
        print("...", self)
        for appointment in appointment_group:
            patient_id = appointment.get("patient_id")[0]
            patient_rec = self.browse(patient_id)
            count = appointment["patient_id_count"]
            patient_rec.appointment_count = count
            self = self - patient_rec
        print("... atfer", self)
        self.appointment_count = 0

    @api.constrains("age")
    def _check_date(self):
        for rec in self:
            if rec.age < 1:
                raise ValidationError(_("The age must be greater than 1"))

    # change username of patient merger with ref
    def name_get(self):
        return [(rec.id, "[%s] %s" % (rec.ref, rec.name)) for rec in self]

    @api.model
    def create(self, vals_list):
        vals_list["ref"] = self.env["ir.sequence"].next_by_code("hospital.patients")
        return super(HospitalPatient, self).create(vals_list)

    def write(self, vals_list):
        print("Write method called from inherited model", vals_list)
        return super(HospitalPatient, self).write(vals_list)

    @api.ondelete(at_uninstall=False)
    def onDelete(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(
                    _("You cannot delete a patient who has appointment")
                )

    def _search_age(self, operator, value):
        dob = date.today() - relativedelta(years=value)

        start = dob.replace(day=1, month=1)

        end = dob.replace(day=31, month=12)

        return [("dob", ">=", start), ("dob", "<=", end)]
