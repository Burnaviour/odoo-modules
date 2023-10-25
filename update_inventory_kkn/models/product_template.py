from odoo import models, fields



class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_minimum_quantity = fields.Boolean("Allow Minimum Quantity", tracking=True)
    minimum_quantity = fields.Integer("Minimum Quantity", tracking=True)
    purchase_description = fields.Text(
        "Purchase Description", translate=True, required=False
    )
    sales_description = fields.Text(
        "Sales Description",
        translate=True,
        required=False,
        help="A description of the Product that you want to communicate to your customers. "
        "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note",
    )
    equipment_type = fields.Selection(
        [
            ("switch", "Switch"),
            ("router", "Router"),
            ("server", "Server"),
            ("odf", "ODF"),
            ("patchpanel", "Patch Panel"),
            ("cablemanager", "Cable Manager"),
            ("antenna", "Antenna"),
            ("wireless", "Wireless"),
            ("radio", "Radio"),
        ],
        string="Equipment Type",
    )
    type_manageable = fields.Selection(
        [("manageable", "Manageable"), ("non_manageable", "Non-Manageable")],
        string="Type",
    )
    rack_mountable = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Rack Mountable"
    )
    is_rack = fields.Boolean(string="Is Rack", default=False)
    rack_space = fields.Integer(string="Rack Space", default=0)
    rack_space_uom = fields.Many2one(
        "uom.uom",
        string="UoM",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "U")]).id,
    )

    is_tower = fields.Boolean(string="Is Tower", default=False)
    power_type = fields.Selection([("AC", "AC"), ("DC", "DC")], string="Power Type")
    total_ampere = fields.Integer(string="Total Power Output", default=0)
    ampere_uom1 = fields.Many2one(
        "uom.uom",
        string="UoM",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "Ampere")]).id,
    )
    running_load = fields.Integer(string="Running Load", default=0)
    ampere_uom2 = fields.Many2one(
        "uom.uom",
        string="UoM",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "Ampere")]).id,
    )
    rated_load = fields.Integer(string="Rated Load", default=0)
    ampere_uom3 = fields.Many2one(
        "uom.uom",
        string="UoM",
        default=lambda self: self.env["uom.uom"].search([("name", "=", "Ampere")]).id,
    )
    uplink_type = fields.Selection(
        [
            ("100M", "100M"),
            ("1G", "1G"),
            ("10G", "10G"),
            ("1G/10G", "1G/10G"),
            ("40G", "40G"),
            ("100G", "100G"),
            ("40G/100G", "40G/100G"),
        ]
    )
    uplink_quantity = fields.Integer()
    downlink_type = fields.Selection(
        [
            ("100M", "100M"),
            ("1G", "1G"),
            ("10G", "10G"),
            ("1G/10G", "1G/10G"),
            ("40G", "40G"),
            ("100G", "100G"),
            ("40G/100G", "40G/100G"),
        ]
    )
    downlink_quantity = fields.Integer()

    uplink_electric_optic = fields.Selection(
        [("Electrical", "Electrical"), ("Optical", "Optical")], string="Uplink Type"
    )
    downlink_electric_optic = fields.Selection(
        [("Electrical", "Electrical"), ("Optical", "Optical")], string="Downlink Type"
    )

    uplink_port_name = fields.Char(string="Uplink Port Name")
    downlink_port_name = fields.Char(string="Downlink Port Name")

    uplink_switch_button = fields.Boolean(default=False)
    downlink_switch_button = fields.Boolean(default=False)
    last_purchase_price = fields.Float("Last Purchase Price")
