# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied
from odoo.exceptions import UserError, ValidationError
import datetime

# AVAILABLE_PRIORITIES = [
#     ('0', 'Low'),
#     ('1', 'Medium'),
#     ('2', 'High'),
#     ('3', 'Very High'),
# ]

STATES = [
    ('draft', 'Draft'),
    ('admin', 'Admin Approval'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancel', 'Cancel'),
]


class kkn_electricity_meters_module(models.Model):
    _name = 'electricity.meters.model'
    _description = 'electricity_meters_model'
    _inherit = 'mail.thread', 'mail.activity.mixin'
    _rec_name = 'meter_number'

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

    # domain = "[('contact_type', '=', 'vendor'), ('active_status', '=', True)]"

    vendor = fields.Many2one('res.partner', required=True, tracking=True,
                             domain="[('contact_type', '=', 'vendor'),('active_status','=',True)]")
    meter_number = fields.Char(string='Meter Number', required=True, tracking=True)
    billing_date = fields.Integer(string='Bill Generation Date', required=True, tracking=True)
    due_date = fields.Integer(string="Due Date", required=True, tracking=True)
    bill_amount = fields.Integer(string='Tentative Billing Amount', tracking=True)

    availability = fields.Selection([
        ('assigned', 'Assigned'),
        ('available', 'Available')], string="Availability", default='available', tracking=True)
    is_created = fields.Boolean(default=False)
    product_template_id = fields.Many2one('product.template', string="Product")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    draft_date = fields.Datetime(string="Draft Date", default=datetime.datetime.today())
    admin_approval_date = fields.Datetime(string="Admin Approval Date")
    approval_date = fields.Datetime(string="Approved Date")
    rejected_date = fields.Datetime(string="Rejected Date")
    cancel_date = fields.Datetime(string="Cancelled Date")
    draft_admin_time = fields.Char(string="Draft to Admin Approval Time")
    admin_to_approve_time = fields.Char(string="Admin to Approve Time")

    def draft_state_method(self):
        # code for draft state method
        self.set_state_draft()

    def admin_approval_state_method(self):
        # code for admin_approval state method
        self.set_state_admin_approval()

    def approved_state_method(self):
        # code for assigned state method
        self.set_state_approved()

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

    def set_state_rejected(self):
        self.state = "rejected"

    def set_state_cancel(self):
        self.state = "cancel"
