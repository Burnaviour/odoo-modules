# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied
from odoo.exceptions import UserError, ValidationError
import datetime
from dateutil.relativedelta import relativedelta

# AVAILABLE_PRIORITIES = [
#     ('0', 'Low'),
#     ('1', 'Medium'),
#     ('2', 'High'),
#     ('3', 'Very High'),
# ]

STATES = [
    ('draft', 'Draft'),
    ('admin', 'Admin Approval'),
    ('iaapproval', 'IA Approval'),
    ('approved', 'Approved'),
    ('cancel', 'Cancel'),
]


class kkn_bills_electricity_module(models.Model):
    _name = 'bills.electricity.model'
    _description = 'bills_electricity_model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

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
            ("iaapproval", "blue"),
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

    date_start = fields.Date(string='Date From', required=True, readonly=True,
                             states={'draft': [('readonly', False)]},
                             default=datetime.date.today().replace(day=1) - relativedelta(months=1))
    date_end = fields.Date(string='Date To', required=True, readonly=True,
                           states={'draft': [('readonly', False)]},
                           default=datetime.date.today().replace(day=1) - datetime.timedelta(days=1))
    name = fields.Char(required=False, readonly=True,
                       default="Electricity Bill " + (datetime.date.today().replace(day=1) -
                                                      datetime.timedelta(days=1)).strftime("%b") + ' ' +
                               str((datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).year), )

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True,
                                  required=False)

    product_template_id = fields.Many2one(related='electricity_card_number.product_template_id', tracking=True)
    amount_total = fields.Monetary(string='Total Bill', store=True, readonly=True, tracking=4)

    pop_id = fields.Many2one('add.pop.model', store=True, required=True, tracking=True)
    meter_number = fields.Many2one('electricity.meters.model', string='Meter Number', required=True, tracking=True)
    vendor = fields.Many2one(related='meter_number.vendor', readonly=1, store=True, string='Vendor', tracking=True)
    billing_date = fields.Integer(related='meter_number.billing_date', readonly=1, store=True, string='Billing Date',
                                  tracking=True)
    due_date = fields.Integer(related='meter_number.due_date', readonly=1, store=True, string='Due Date', tracking=True)
    bill_amount = fields.Integer(related='meter_number.bill_amount', readonly=0, store=True,
                                 string='Tentative Billing Amount', tracking=True)
    product_template_id = fields.Many2one(related='meter_number.product_template_id', tracking=True)

    bills_id = fields.Many2one('account.move', string="Electricity Bills ID")
    bill_state = fields.Selection([
        ('not_bill', "Not Billed"),
        ('draft', "Draft"),
        ('COO Approval', "COO Approval"),
        ('CEO Approval', "CEO Approval"),
        ('checked', "Checked"),
        ('Internal Audit', "Audited"),
        ('posted', "Posted"),
        ('cancel', "Cancel"),
    ], string="Bill Status", default='not_bill')
    bill_payment_state = fields.Selection([
        ('not_bill', "Not Billed"),
        ('not_paid', "Not Paid"),
        ('in_payment', "In Payment"),
        ('paid', "Paid"),
    ], string="Bill Payment Status", default='not_bill')
    draft_date = fields.Datetime(string="Draft Date", default=datetime.datetime.today())
    admin_approval_date = fields.Datetime(string="Admin Approval Date")
    approval_date = fields.Datetime(string="Approved Date")
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

    def iaapproval_state_method(self):
        # code for unassign_request state method
        self.set_state_iaapproval()

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

    def set_state_iaapproval(self):
        self.state = "iaapproval"

    def set_state_cancel(self):
        self.state = "cancel"
