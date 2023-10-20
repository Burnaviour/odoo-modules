# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Patient_Tag (models. Model):
    _name = "patient.tag"
    _description = "Patient Tag"
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string="Active", default=True, copy=False)

    color = fields.Integer(string='Color Index')
    sequence = fields.Integer(string='Sequence')
    # color2=fields.Char(string='Color ')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (Copy)") % self.name
        default['sequence'] = 10
        return super(Patient_Tag, self).copy(default=default)
    _sql_constraints = [
        ('unique_tag_name', 'unique (name,active)', 'Name Must be Unique!'),
        ('unique_tag_sequence', 'check(sequence >0)', 'Sequence Must be grater than 0!'
         ),
    ]
