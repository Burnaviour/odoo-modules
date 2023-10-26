# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied
from odoo.exceptions import UserError, ValidationError
import datetime

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class kkn_electricity_meters_module(models.Model):
    _name = 'electricity_meters_module'
    _description = 'electricity_meters_module'
    _inherit = 'mail.thread', 'mail.activity.mixin'
    _rec_name = 'meter_number'

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
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancel'),
    ], string='State', required=1, group_expand='_expand_states', default='draft', tracking=True)

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

    # def admin_approval(self):
    #
    #     self.state = 'admin'
    #     self.admin_approval_date = datetime.datetime.today()
    #     if self.admin_approval_date and self.draft_date:
    #         delta = self.admin_approval_date - self.draft_date
    #         sec = delta.total_seconds()
    #         self.draft_admin_time = sec / (60 * 60)
    #
    # def reset_to_draft(self):
    #
    #     self.state = 'draft'
    #     self.draft_date = datetime.datetime.today()
    #
    # def approved(self):
    #
    #     # vals = {
    #     #     'name': "Electricity Bill - " + self.meter_number,
    #     #     'sale_ok': False,
    #     #     'purchase_ok': True,
    #     #     'can_be_expensed': True,
    #     #     'type': 'consu',
    #     #     'categ_id': self.env['product.category'].search([('is_electricitybill', '=', True)]).id,
    #     #     'description_purchase': self.meter_number,
    #     #     'property_account_expense_id': self.env['account.account'].search([('code', '=', '200110010003')]).id,
    #     # }
    #     # self.is_created = True
    #     # if self.env['product.template'].search_count([('name', 'ilike', self.meter_number)]) == 0:
    #     #     product_id = self.env['product.template'].create(vals)
    #     #     self.product_template_id = product_id.id
    #
    #     self.state = 'approved'
    #     self.approval_date = datetime.datetime.today()
    #     if self.approval_date and self.admin_approval_date:
    #         delta = self.approval_date - self.admin_approval_date
    #         sec = delta.total_seconds()
    #         self.admin_to_approve_time = sec / (60 * 60)
    #
    # def rejected(self):
    #
    #     self.state = 'rejected'
    #     self.rejected_date = datetime.datetime.today()
    #
    # def cancelled(self):
    #
    #     self.state = 'cancel'
    #     self.cancel_date = datetime.datetime.today()
