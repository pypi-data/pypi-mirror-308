from odoo import api, Command, fields, models, _
import datetime


WORK_ORDER_STATUS = [
    ('draft', 'Draft'),
    ('queue', "In Queue"),
    ('delay', "Delayed"),
    ('done', "Work Complete"),
]


class WorkOrder(models.Model):
    _inherit = 'sale.order'
    _description = """Work Order"""
    _order = 'date_deadline asc, state, date_order asc, create_date asc, id desc'

    bike_id = fields.Many2one(
        string='Bicycle', comodel_name='bikeshop.bicycle')
    customer_request = fields.Text(string='Customer Request')
    evaluation = fields.Text(string='Evaluation')
    notes = fields.Text(string='Internal Notes')
    wo_status = fields.Selection(
        selection=WORK_ORDER_STATUS,
        string="WO Status",
        copy=False, index=True,
        default='draft')
    labor_hours = fields.Float(string='Book Hours',
                               digits='Product Unit of Measure',
                               store=True,
                               compute='_compute_labor_hours')
    delay_reason = fields.Many2one(string='Delay Reason',
                                   comodel_name='bikeshop.delay_reason',
                                   ondelete='set null')
    display_state = fields.Char(string='Repair Status',
                                compute='_compute_display_state',
                                store=True)
    date_deadline = fields.Date(string='Due Date',
                                compute='_compute_date_deadline',
                                inverse='_compute_inverse_date_deadline',
                                store=True)
    partner_id_contact_method = fields.Selection(
        related="partner_id.contact_method",
        store=False)
    partner_id_email = fields.Char(related="partner_id.email",
                                   store=True,
                                   depends=['partner_id'])
    partner_id_phone = fields.Char(related="partner_id.phone",
                                   store=True,
                                   depends=['partner_id'])
    partner_id_mobile = fields.Char(related="partner_id.mobile",
                                    store=True,
                                    depends=['partner_id'])

    def action_draft(self):
        """
        Set the work order status and the overall sale order state to "draft".
        """

        self.write({'wo_status': 'draft'})
        return super().action_draft()

    def action_delay_repair(self):
        """
        Mark the repair as delayed and open a wizard to pick a reason for the
        delay.
        """

        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Delay Reason'),
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('bikeshop.sale_order_view_delay_reason').id,
            'target': 'new',
        }

    def action_set_delay_reason(self):
        """
        Sets the delay reason when the delay reason wizards save button has been
        clicked.
        """

        self.ensure_one()

        self._get_repair_activity().unlink()
        self.update({
            'wo_status': 'delay',
        })

    def action_schedule_repair(self):
        """
        Open the activity creation form with the defaults set for scheduling a
        new repair activity.
        """

        self.ensure_one()

        model = self.env['ir.model'].search(
            [('model', '=', self._name)],
            limit=1,
        )
        act_type_id = self.env.ref('bikeshop.mail_activity_bikeshop_repair').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Schedule Repair',
            'res_model': 'mail.activity',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'default_res_id': self.id,
                'default_res_model_id': model.id,
                'default_activity_type_id': act_type_id,
            },
        }

    def action_finish_repair(self):
        """
        Finish the repair by closing any open repair activity.
        """

        act = self._get_repair_activity()
        act.action_feedback()
        return True

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.bike_id.owner_id != self.partner_id:
            self.update({
                'bike_id': None,
            })

    @api.onchange("bike_id")
    def _onchange_bike_id(self):
        if self.bike_id.owner_id != self.partner_id:
            self.update({
                'partner_id': self.bike_id.owner_id,
            })

    @api.depends('order_line.product_id')
    def _compute_labor_hours(self):
        for order in self:
            order_lines = order.order_line.filtered(
                lambda x: not x.display_type)
            total = 0.0
            for line in order_lines:
                total += line.product_id.labor_hours * line.product_uom_qty
            order.update({
                'labor_hours': total,
            })

    @api.depends('state', 'wo_status', 'delay_reason')
    def _compute_display_state(self):
        state_dict = dict(self._fields['state'].selection)
        wo_status_dict = dict(self._fields['wo_status'].selection)

        for record in self:
            if record.wo_status == 'draft' or record.state == 'cancel':
                record.update({
                    'display_state': state_dict.get(record.state),
                })
            else:
                if record.wo_status == 'delay':
                    wostatus = wo_status_dict.get(record.wo_status)
                    record.update({
                        'display_state': _(f'Delayed {record.delay_reason.name}'),
                    })
                else:
                    record.update({
                        'display_state': wo_status_dict.get(record.wo_status),
                    })

    @api.depends('activity_ids.date_deadline')
    def _compute_date_deadline(self):
        for record in self:
            act = record._get_repair_activity()
            if act:
                record.update({
                    'date_deadline': act.date_deadline,
                })
            else:
                record.update({
                    'date_deadline': False,
                })

    def _compute_inverse_date_deadline(self):
        for record in self:
            act = record._get_repair_activity()
            if act:
                # If an activity already exists in the calendar for this repair
                # order, unlink it if we've deleted the deadline or reschedule
                # it if we've set a new deadline.
                if record.date_deadline:
                    record.activity_reschedule(
                        ['bikeshop.mail_activity_bikeshop_repair'],
                        user_id=None,
                        date_deadline=record.date_deadline,
                        new_user_id=None)
                else:
                    record.activity_unlink(
                        ['bikeshop.mail_activity_bikeshop_repair'],
                        user_id=None)
            else:
                # If there was not already a calendar activity created and we're
                # setting a deadline, schedule a matching activity on the
                # calendar with the same deadline.
                if record.date_deadline:
                    # There shouldn't be any activities at this point, but for
                    # some reason it keeps complaining about duplicates, so
                    # unlink them first.
                    record.activity_unlink(
                        ['bikeshop.mail_activity_bikeshop_repair'],
                        user_id=None)
                    record.activity_schedule(
                        act_type_xmlid='bikeshop.mail_activity_bikeshop_repair',
                        date_deadline=record.date_deadline,
                        user_id=None)

    def _get_repair_activity(self):
        """
        Gets the bicycle repair if already scheduled.
        """

        try:
            act_type_id = self.env.ref(
                'bikeshop.mail_activity_bikeshop_repair').id
        except ValueError:
            # If demo data is loaded before the module is fully installed, we'll
            # try to compute the deadline, but the activity type won't exist yet
            # causing things to fail.
            # In this case, just return "none" and we just won't have a deadline
            # set in the demo data.
            return None
        return self.activity_ids.search([('res_id', '=', self.id),
                                        ('activity_type_id', '=', act_type_id)])
