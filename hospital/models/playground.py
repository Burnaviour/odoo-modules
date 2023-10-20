# -*- coding: utf-8 -*-
from docutils.nodes import document

from odoo import models, fields, api
from odoo.tools.convert import safe_eval


class Playground(models.Model):
    _name = "hospital.playground"
    _description = 'Hospital Playground'
    DEFAULT_ENV_VARIABLE = """
# Available variables:
#self: Current Object
# self.env: Odoo Environment on which the action is triggered
# - self.env.user: Return the current user (as an instance)
# - self.env.is_system: Return whether the current user has group "Settings", or is in superuser mode.
# self.env.is_admin: Return whether the current user has group "Access Rights", or is in superuser mode.
# - self.env.ts_superuser: Return whether the environment is in superuser mode.
# - self.env.company: Return the current company (as an instance)
#- self.env.companies: Return a recordset of the enabled companies by the user.
# - self.env.lang: Return the current language code \n\n\n 
    """
    name=fields.Char(string='Name')
    code = fields.Char(string='Code', default=DEFAULT_ENV_VARIABLE)
    description = fields.Text(string='Description')
    result = fields.Text(string='Result')

    def execute_code(self):
        for rec in self:
            try:
                result = safe_eval(rec.code.strip(), {'env': self.env, 'self': rec})
                rec.result = str(result)
            except Exception as e:
                rec.result = str(e)
        return True

