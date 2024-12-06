from odoo import api, models


class Followers(models.Model):
    _inherit = 'mail.followers'

    @api.model_create_multi
    def create(self, vals_list):
        # Fixes a duplicate insertion into the database when creating a new work
        # order with a due-date already set. It is unclear to me why this would
        # be a problem or why we'd need to de-duplicate this, so this is likely
        # a bad bandaid over the problem. If anyone else knows why this would be
        # an issue, please let me know.
        for vals in vals_list:
            if 'res_model' in vals and 'res_id' in vals and 'partner_id' in vals:
                dups = self.env['mail.followers'].search([('res_model', '=', vals.get('res_model')),
                                                          ('res_id', '=',
                                                           vals.get('res_id')),
                                                          ('partner_id', '=', vals.get('partner_id'))])
                if len(dups):
                    for p in dups:
                        p.unlink()
        res = super(Followers, self).create(vals)
        return res
