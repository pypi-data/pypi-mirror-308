from odoo import api, models


class MailActivity(models.Model):
    """
    Override the mail activity to update the state of any attached work orders
    when the activity is created or destroyed.
    """

    _inherit = 'mail.activity'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Set the work order state to "queue" when a new activity of the correct
        type is attached to it.
        """

        records = super(MailActivity, self).create(vals_list)
        records._do_wo(lambda res: res.update({'wo_status': 'queue'}))
        return records

    def action_feedback(self, feedback=False, attachment_ids=None):
        """
        Set the attached work order to the "done" status when the activity is
        marked as complete.
        """

        for act in self:
            act._do_wo(lambda res: res.update({'wo_status': 'done'}))
        return super(MailActivity, self).action_feedback(feedback=feedback,
                                                         attachment_ids=attachment_ids)

    @api.ondelete(at_uninstall=False)
    def _reset_wo_state_on_unlink(self):
        """
        When the activity is canceled, set the attached work order to status
        "draft".
        """

        for act in self:
            if act.state != 'done':
                act._do_wo(lambda res: res.update({'wo_status': 'draft'}))

    def _do_wo(self, λ):
        """
        Check if this activity is a bicycle activity on a work order.
        If so, execute the lambda passing it the work order.
        """

        model = self.env['ir.model'].search(
            [('model', '=', 'sale.order')],
            limit=1,
        )
        act_type_id = self.env.ref('bikeshop.mail_activity_bikeshop_repair').id
        for act in self:
            resmod = self.env[act.res_model].browse(act.res_id)
            if resmod and act.activity_type_id.id == act_type_id and act.res_model_id.id == model.id:
                λ(resmod)
