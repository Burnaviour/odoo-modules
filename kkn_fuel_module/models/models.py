# -*- coding: utf-8 -*-

from odoo import models, fields, api


STATES = [
    ("draft", "Draft"),
    ("admin", "Admin Approval"),
    ("approved", "Assigned"),
    ("unassign", "Unassigned"),
    ("rejected", "Rejected"),
    ("cancel", "Cancel"),
]


class AssignFuelCard(models.Model):
    _name = "assign.fuel.card.model"
    _description = "Assign Fuel Card to employees"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    _rec_name = "employee_id"
    employee_id = fields.Many2one("hr.employee")

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
    state = fields.Selection(
        STATES,
        string="State",
        required=1,
        default="draft",
        tracking=True,
        group_expand='_expand_states',
    )
