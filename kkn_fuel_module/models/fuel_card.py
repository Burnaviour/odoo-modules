from datetime import datetime
import logging
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# from lxml import etree
# import json

_logger = logging.getLogger(__name__)


STATES = [
    ("draft", "Draft"),
    ("admin_approval", "Admin Approval"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("cancel", "Cancelled"),
]

MIN_FUEL_LIMIT = 1


class CreateFuelCard(models.Model):
    _name = "create.fuel.card.model"
    _description = "Create Fuel Cards"
    _rec_name = "card_number"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    card_number = fields.Char(
        string="Card Number",
        required=True,
    )
    name_on_card = fields.Char(
        string="Name on Card",
        required=True,
    )
    product_name = fields.Selection(
        [
            ("premier_euro5", "Premier Euro5"),
            ("hi_octane", "Hi-Octane"),
            ("hi_cetane", "Hi-Cetane"),
            ("hi_octane_euro5", "Hi-Octane + Euro5"),
        ],
        default="premier_euro5",
        required=True,
        tracking=True,
    )
    card_usage_limit = fields.Integer(
        string="Card Limit(Liters)",
        required=True,
        default=MIN_FUEL_LIMIT,
    )
    valid_from_month = fields.Selection(
        [
            ("01", "01"),
            ("02", "02"),
            ("03", "03"),
            ("04", "04"),
            ("05", "05"),
            ("06", "06"),
            ("07", "07"),
            ("08", "08"),
            ("09", "09"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
        required=True,
        string="Valid From",
        default="01",
    )
    valid_from_year = fields.Selection(
        [(str(num), str(num)) for num in range(2020, (datetime.now().year) + 10)],
        required=True,
        default=str(datetime.now().year),
    )
    valid_till_month = fields.Selection(
        [
            ("01", "01"),
            ("02", "02"),
            ("03", "03"),
            ("04", "04"),
            ("05", "05"),
            ("06", "06"),
            ("07", "07"),
            ("08", "08"),
            ("09", "09"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
        required=True,
        string="Valid Till",
        default="12",
    )
    valid_till_year = fields.Selection(
        [(str(num), str(num)) for num in range(2020, (datetime.now().year) + 10)],
        required=True,
        default=str(datetime.now().year),
    )

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
        compute="_compute_kanban_state_label",
        string="Kanban State Label",
        store=True,
    )

    is_assigned = fields.Boolean(string="Assigned", tracking=True, default=False)

    _sql_constraints = [
        ("card_number_unique", "unique(card_number)", "Card number already exist!"),
    ]

    @api.constrains("card_usage_limit")
    def _check_fuel_limit(self):
        for record in self:
            if record.card_usage_limit < MIN_FUEL_LIMIT:
                raise ValidationError(
                    _("Fuel limit should be greater than or equal to 1")
                )

    @api.depends("state", "kanban_state")
    def _compute_kanban_state_label(self):
        for task in self:
            task.kanban_state = task.state
            task.kanban_state_label = task.state

    def draft_state_method(self):
        # code for draft state method
        for record in self:
            record.set_state_draft()

    def admin_approval_state_method(self):
        # code for admin_approval state method
        for record in self:
            record.set_state_admin_approval()

    def approved_state_method(self):
        # code for approved state method
        for record in self:
            record.set_state_approved()

    def rejected_state_method(self):
        # code for rejected state method
        for record in self:
            record.set_state_rejected()

    def cancel_state_method(self):
        # code for cancel state method
        for record in self:
            record.set_state_cancel()

    # state setter methods
    def set_state_draft(self):
        self.state = "draft"

    def set_state_admin_approval(self):
        self.state = "admin_approval"

    def set_state_approved(self):
        self.state = "approved"

    def set_state_rejected(self):
        self.state = "rejected"

    def set_state_cancel(self):
        self.state = "cancel"

    # @api.model
    # def get_view(self, view_id=None, view_type="form", **options):
    #     context = self._context
    #     _logger.error("%s", context)
    #     res = super().get_view(view_id=view_id, view_type=view_type, **options)
    #     if view_type == "form" and (
    #         context.get("active_id")
    #         and self.browse(context.get("active_id")).state != "draft"
    #     ):
    #         doc = etree.XML(res["arch"])
    #         # Applies only for form view
    #         for node in doc.xpath("//field"):
    #             # All the view fields to readonly
    #             node.set("readonly", "1")
    #             if modifiers := node.get("modifiers"):
    #                 # Check if modifiers is not None
    #                 modifiers = json.loads(modifiers)
    #                 modifiers["readonly"] = True
    #                 # print(modifiers)
    #                 node.set("modifiers", json.dumps(modifiers))

    #         res["arch"] = etree.tostring(doc, encoding="unicode")
    #     return res
