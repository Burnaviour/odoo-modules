# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard (models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    def default_get(self, fields_list):
        res = super(CancelAppointmentWizard, self).default_get(fields_list)
        res['cancel_date'] = fields.datetime.today()
        return res
    appointment_id = fields.Many2one(
        'hospital.appointment', string="Appointment", required=True)
    reason = fields.Text(string="Reason", default="Not Satisfied")
    cancel_date = fields.Date(string="Cancel Date")

    def action_cancel(self):

        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_("You cannot cancel today's appointment"))
        else:
            self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
            
