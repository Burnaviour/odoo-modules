from odoo import models, fields, api
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    company_id = fields.Many2one(
        'res.company', 'Company', index=True,default=lambda self: self.env.company)


