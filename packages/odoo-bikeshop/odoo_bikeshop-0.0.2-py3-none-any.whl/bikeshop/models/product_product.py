from odoo import fields, models


class Product(models.Model):
    _inherit = 'product.product'
    _description = 'Product Variant that includes book hours for labor'

    labor_hours = fields.Float(
        string='Book Hours', digits='Product Unit of Measure')
