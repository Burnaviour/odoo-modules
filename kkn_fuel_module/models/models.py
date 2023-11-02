# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


STATES = [
    ("draft", "Draft"),
    ("admin_approval", "Admin Approval"),
    ("assigned", "Assigned"),
    ("unassign_request", "Unassign Request"),
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
        group_expand="_expand_states",
    )
    kanban_state = fields.Selection(
        [
            ("draft", "Grey"),
            ("admin_approval", "Yellow"),
            ("assigned", "Green"),
            ("unassign_request", "blue"),
            ("rejected", "Red"),
            ("cancel", "Red"),
        ],
        string="Kanban State",
        copy=False,
        default="draft",
        required=True,
    )
    kanban_state_label = fields.Char(
        compute="_compute_kanban_state_label",
        string="Kanban State Label",
        tracking=True,
    )

    @api.depends("state", "kanban_state")
    def _compute_kanban_state_label(self):
        for task in self:
            if task.state == "draft":
                task.kanban_state = "draft"
                task.kanban_state_label = "draft"
            elif task.state == "assigned":
                task.kanban_state = "assigned"
                task.kanban_state_label = "assigned"
            elif task.state == "admin_approval":
                task.kanban_state = "admin_approval"
                task.kanban_state_label = "admin_approval"
            elif task.state == "unassign_request":
                task.kanban_state = "unassign_request"
                task.kanban_state_label = "unassign_request"
            elif task.state == "rejected":
                task.kanban_state = "rejected"
                task.kanban_state_label = "rejected"
            else:
                task.kanban_state = "cancel"
                task.kanban_state_label = "cancel"
