# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import ValidationError

#Class is Extended for new feature for get projects starting time.
class ProjectTask(models.Model):
    _inherit = "project.task"

    temp_start_date = fields.Datetime('Temp Start Date')  
    active_task = fields.Boolean(default=False)

    def get_project_starting_time(self):
        active_another_task = self.env['project.task'].search([('active_task','=',True)])

        if active_another_task:
            task_name = active_another_task.name
            raise ValidationError('%s task is already in progress ' % task_name)
        else:
            for record in self:
                if record:
                    record.temp_start_date = datetime.now()
                    record.active_task = True

