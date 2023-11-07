from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


STATES = [
    ("draft", "Draft"),
    ("admin_approval", "Admin Approval"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("cancel", "Cancel"),
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
        tracking=True,
    )

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
