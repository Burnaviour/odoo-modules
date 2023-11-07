# -*- coding: utf-8 -*-
from odoo import models, fields, api


STATES = [
    ("draft", "Draft"),
    ("admin_approval", "Admin Approval"),
    ("assigned", "Assigned"),
    ("unassign_request", "Unassign Request"),
    ("unassigned", "Unassigned"),
    ("rejected", "Rejected"),
    ("cancel", "Cancel"),
]


class AssignFuelCard(models.Model):
    _name = "assign.fuel.card.model"
    _description = "Assign Fuel Card to employees"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    _rec_name = "employee_id"
    employee_id = fields.Many2one(
        "hr.employee", string="Employee", required=True, tracking=True
    )
    fuel_card_id = fields.Many2one(
        "create.fuel.card.model",
        string="Card Number",
        domain=[("state", "=", "approved")],
        tracking=True,
        required=True,
    )
    name_on_card = fields.Char(
        related="fuel_card_id.name_on_card",
        string="Name on Card",
        store=True,
    )
    product_name = fields.Selection(
        related="fuel_card_id.product_name",
        string="Product Name",
        store=True,
    )
    card_usage_limit = fields.Integer(
        related="fuel_card_id.card_usage_limit",
        string="Card Limit(Liters)",
        store=True,
    )
    valid_from_month = fields.Selection(
        related="fuel_card_id.valid_from_month",
        string="Valid From (Month/Year)",
        store=True,
    )
    valid_from_year = fields.Selection(
        related="fuel_card_id.valid_from_year",
        store=True,
    )
    valid_till_month = fields.Selection(
        related="fuel_card_id.valid_till_month",
        string="Valid Till (Month/Year)",
        store=True,
    )
    valid_till_year = fields.Selection(
        related="fuel_card_id.valid_till_year",
        store=True,
    )

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    state = fields.Selection(
        STATES,
        string="State",
        required=True,
        default="draft",
        tracking=True,
        group_expand="_expand_states",
    )

    kanban_state = fields.Selection(
        [
            ("draft", "Grey"),
            ("admin_approval", "Yellow"),
            ("assigned", "Green"),
            ("unassigned", "Red"),
            ("unassign_request", "Blue"),
            ("rejected", "Red"),
            ("cancel", "Red"),
        ],
        string="Kanban State",
        copy=False,
        default="draft",
        required=True,
    )
    kanban_state_label = fields.Char(
        compute="_compute_kanban_state_label", string="Kanban State Label", store=True
    )

    @api.depends("state", "kanban_state")
    def _compute_kanban_state_label(self):
        for task in self:
            task.kanban_state = task.state
            task.kanban_state_label = task.state

    def draft_state_method(self):
        # code for draft state method
        self.set_state_draft()

    def admin_approval_state_method(self):
        # code for admin_approval state method
        self.set_state_admin_approval()

    def assigned_state_method(self):
        # code for assigned state method
        self.set_state_assigned()

    def unassign_request_state_method(self):
        # code for unassign_request state method
        self.set_state_unassign_request()

    def unassigned_state_method(self):
        # code for unassigned state method
        self.set_state_unassigned()

    def rejected_state_method(self):
        # code for rejected state method
        self.set_state_rejected()

    def cancel_state_method(self):
        # code for cancel state method
        self.set_state_cancel()

    # state setter methods
    def set_state_draft(self):
        self.state = "draft"

    def set_state_admin_approval(self):
        self.state = "admin_approval"

    def set_state_assigned(self):
        self.state = "assigned"

    def set_state_unassign_request(self):
        self.state = "unassign_request"

    def set_state_unassigned(self):
        self.state = "unassigned"

    def set_state_rejected(self):
        self.state = "rejected"

    def set_state_cancel(self):
        self.state = "cancel"
