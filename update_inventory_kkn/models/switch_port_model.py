from odoo import models, fields


class SwitchPortUp(models.Model):
    _name = "switch.port.up"
    _rec_name = "port"
    port = fields.Char(string="Port")
    assigned_status = fields.Boolean()
    serial_no = fields.Char()
