from odoo import fields, models

PREFERRED_CONTACT_METHOD = [
    ('phone_call', "Phone Call"),
    ('phone_text', "Text Message"),
    ('email', 'Email'),
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bike_ids = fields.One2many(string='Bikes',
                               comodel_name='bikeshop.bicycle',
                               inverse_name='owner_id')
    workorder_id = fields.One2many(string='Work Orders',
                                   comodel_name='sale.order',
                                   inverse_name='partner_id')
    contact_method = fields.Selection(
        selection=PREFERRED_CONTACT_METHOD,
        string="Contact Preference",
        default='phone_call')
