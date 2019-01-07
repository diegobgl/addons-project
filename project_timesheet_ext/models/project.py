# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging


from odoo.exceptions import UserError

_logger = logging.getLogger(__name__) # Need for message in console.


class Task(models.Model):
    _inherit = "project.task"

    @api.multi
    def action_hr_timesheet_b(self):
        for record in self:

            if record.planned_hours > 0 and record.user_id.employee_ids.id:
                self.env['account.analytic.line'].create({
                    'name': "%s (%s)" % (record.name or '', record.planned_hours),
                    'project_id': record.project_id.id,
                    'task_id': record.id,
                    'unit_amount': record.planned_hours,
                    'employee_id': record.user_id.employee_ids.id,
                    'user_id':record.user_id.id,
                })
            else:
                raise UserError(_(
                    'You can not add a Timesheet.\nPlease enter planned_hours'))

        return True



