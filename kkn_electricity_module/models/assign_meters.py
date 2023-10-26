# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
from odoo.exceptions import AccessDenied
from odoo.exceptions import UserError, ValidationError

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class kkn_electricity_module(models.Model):
    _name = 'assign_electricity_module'
    _description = 'assign_electricity_module'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'pop_id'

    color = fields.Integer('Color Index')
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State',
        copy=False, default='normal', required=True)
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', index=True, default=AVAILABLE_PRIORITIES[0][0])

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    state = fields.Selection([
        ('draft', 'Draft'),
        ('admin', 'Admin Approval'),
        ('approved', 'Assigned'),
        ('unassign', 'Unassigned'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancel'),
    ], string='State', required=1, group_expand='_expand_states', default='draft', tracking=True)

    pop_id = fields.Many2one('add_pop_module', store=True, required=True, tracking=True)
    meter_number = fields.Many2one('electricity_meters_module', string='Meter Number', required=True, tracking=True)
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
