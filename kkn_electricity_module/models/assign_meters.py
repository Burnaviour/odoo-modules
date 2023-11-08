# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
from odoo.exceptions import AccessDenied
from odoo.exceptions import UserError, ValidationError

# AVAILABLE_PRIORITIES = [
#     ('0', 'Low'),
#     ('1', 'Medium'),
#     ('2', 'High'),
#     ('3', 'Very High'),
# ]

STATES = [
    ('draft', 'Draft'),
    ('admin', 'Admin Approval'),
    ('approved', 'Assigned'),
    ('unassign', 'Unassigned'),
    ('rejected', 'Rejected'),
    ('cancel', 'Cancel'),
]


class kkn_electricity_module(models.Model):
    _name = 'assign.electricity.model'
    _description = 'assign.electricity.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'pop_id'

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

    # color = fields.Integer("Color Index")
    # priority = fields.Selection(
    #     AVAILABLE_PRIORITIES,
    #     string="Priority",
    #     index=True,
    #     default=AVAILABLE_PRIORITIES[0][0],
    # )

    kanban_state = fields.Selection(
        [
            ("draft", "Grey"),
            ("admin", "Yellow"),
            ("approved", "Green"),
            ("unassign", "Red"),
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

    pop_id = fields.Many2one('add.pop.model', store=True, required=True, tracking=True)
    meter_number = fields.Many2one('electricity.meters.model', string='Meter Number', required=True, tracking=True)
    vendor = fields.Many2one(related='meter_number.vendor', readonly=1, store=True, string='Vendor', tracking=True)
    billing_date = fields.Integer(related='meter_number.billing_date', readonly=1, store=True, string='Billing Date',
                                  tracking=True)
    due_date = fields.Integer(related='meter_number.due_date', readonly=1, store=True, string='Due Date', tracking=True)
    bill_amount = fields.Integer(related='meter_number.bill_amount', readonly=1, store=True,
                                 string='Tentative Billing Amount', tracking=True)

    availability = fields.Selection([
        ('assigned', 'Assigned'),
        ('available', 'Available')], string="Availability", default='available', tracking=True)

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    draft_date = fields.Datetime(string="Draft Date", default=datetime.datetime.today())
    admin_approval_date = fields.Datetime(string="Admin Approval Date")
    assign_date = fields.Datetime(string="Assign Date")
    rejected_date = fields.Datetime(string="Rejected Date")
    cancel_date = fields.Datetime(string="Cancelled Date")
    draft_admin_time = fields.Char(string="Draft to Admin Approval Time")
    admin_to_assign_time = fields.Char(string="Admin to Assign Time")


    def draft_state_method(self):
        # code for draft state method
        self.set_state_draft()

    def admin_approval_state_method(self):
        # code for admin_approval state method
        self.set_state_admin_approval()

    def approved_state_method(self):
        # code for assigned state method
        self.set_state_approved()

    def unassign_state_method(self):
        # code for unassign_request state method
        self.set_state_unassign()

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
        self.state = "admin"

    def set_state_approved(self):
        self.state = "approved"

    def set_state_unassign(self):
        self.state = "unassign"

    def set_state_rejected(self):
        self.state = "rejected"

    def set_state_cancel(self):
        self.state = "cancel"
