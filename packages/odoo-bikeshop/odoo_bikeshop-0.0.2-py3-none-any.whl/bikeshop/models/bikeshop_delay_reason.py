from odoo import fields, models


class BikeshopDelayReason(models.Model):
    """
    Delay reasons are selectable reasons for why a work order has been delayed.
    """
    _name = 'bikeshop.delay_reason'
    _description = 'Delay Reason'
    _order = 'name, id'

    name = fields.Char('Name', required=True, translate=True)
