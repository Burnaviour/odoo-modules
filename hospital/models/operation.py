from odoo import _, api, fields, models


class Operations(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """

    _name = "hospital.operations"
    _description = "Hospital Operations"
    _rec_name = "op_name"
    _log_access = False
    _order = 'sequence'
    doctor_id = fields.Many2one("res.users", string="Doctor")
    op_name = fields.Char(string="Name")

    sequence = fields.Integer(string="Sequence", default=10)

    @api.model
    def name_create(self, name):
        return self.create({"op_name": name}).name_get()[0]
