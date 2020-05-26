# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    checklist_name = fields.Char(string='Checklist name')
    checklist_item_ids = fields.One2many('project_task_checklist.item', 'task_id', string='Checklist elements', copy=True)
