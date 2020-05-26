# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class ProjectTaskChecklistItem(models.Model):
    _name = 'project_task_checklist.item'
    _description = 'Task Checklist Item'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    task_id = fields.Many2one('project.task', string='Task', index=True)
    company_id = fields.Many2one(related='task_id.company_id', string='Company', store=True, readonly=True)
    name = fields.Char(string='Name', required=True)
    checked = fields.Boolean('Checked')
