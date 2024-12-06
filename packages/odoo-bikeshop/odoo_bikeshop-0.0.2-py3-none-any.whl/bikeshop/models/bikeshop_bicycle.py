from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Bicycle(models.Model):
    _name = "bikeshop.bicycle"
    _description = "A customer owned bicycle"
    _rec_name = 'serial'

    serial = fields.Char(string='Serial Number',
                         required=True, index='btree', copy=False)
    color = fields.Char(string='Color', required=True, translate=True)
    make = fields.Char(string='Make', required=True)
    model = fields.Char(string='Model', required=True)
    # Use a char instead of an int so that it can be empty instead of defaulting
    # to 0. This is a bit jank feeling, but works well enough for simple data.
    model_year = fields.Char(string='Year')
    derailleur_hanger = fields.Char(string='Derailleur Hanger')
    owner_id = fields.Many2one(
        string='Owner', comodel_name='res.partner', ondelete='set null')
    battery_key = fields.Char(string='Battery Key', required=False)
    notes = fields.Text(string='Notes', required=False)
    display_name = fields.Char(compute='_compute_display_name', store=True)
    workorder_id = fields.One2many(string='Work Orders',
                                   comodel_name='sale.order',
                                   inverse_name='bike_id')

    _sql_constraints = [
        ('unique_sn', 'UNIQUE (serial)',
         'Bicycle serial numbers should be unique.'),
    ]

    @api.depends('color', 'make', 'model')
    def _compute_display_name(self):
        for record in self:
            record.update({
                'display_name': _(f"{record.color} {record.make} {record.model}"),
            })

    @api.constrains('model_year')
    def _check_model_year(self):
        for record in self:
            if record.model_year != '':
                try:
                    int(record.model_year)
                except ValueError:
                    raise ValidationError(
                        "Model year field must be an integer year")
