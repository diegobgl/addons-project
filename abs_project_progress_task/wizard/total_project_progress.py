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

from odoo import api, fields,tools, models,_
from datetime import date, datetime ,timedelta

#Class is Extended for new feature for create wizard of worked hours and descriptions.
class ProjectProgress(models.TransientModel):
    _name = 'project.progress'

    description = fields.Char('Description',required=True)
    duration = fields.Float('Worked Hours',compute='get_task_time_difference')

    #Display duration of that project.
    @api.depends('description')
    def get_task_time_difference(self):
        end_date = datetime.now()
        active_id=self.env.context.get('active_id',False)
        task_id = self.env['project.task'].search([('id','=',active_id)])
        start_date = task_id.temp_start_date

        if start_date:
            from_time = float('%s.%s' % (datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%H'), datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%M')))
            from_time = float(int(from_time) +(100*(from_time - int(from_time)))/60)
            to_time = float('%s.%s' % (datetime.strptime(str(end_date)[:-7], '%Y-%m-%d %H:%M:%S').strftime('%H'), datetime.strptime(str(end_date)[:-7], '%Y-%m-%d %H:%M:%S').strftime('%M')))
            to_time = float(int(to_time) +(100*(to_time - int(to_time)))/60)
            differrence = to_time - from_time
        self.duration = differrence

    #Add all deatils and worked duration on task timesheet.
    @api.multi
    def add_detail_in_timesheet(self):
        end_date = datetime.now()
        active_id=self.env.context.get('active_id',False)
        task_id = self.env['project.task'].search([('id','=',active_id)])
        start_date = task_id.temp_start_date
        account_analytic = self.env['account.analytic.line']

        for record in self:
            if start_date:
                from_time = float('%s.%s' % (datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%H'), datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%M')))
                from_time = float(int(from_time) +(100*(from_time - int(from_time)))/60)
                to_time = float('%s.%s' % (datetime.strptime(str(end_date)[:-7], '%Y-%m-%d %H:%M:%S').strftime('%H'), datetime.strptime(str(end_date)[:-7], '%Y-%m-%d %H:%M:%S').strftime('%M')))
                to_time = float(int(to_time) +(100*(to_time - int(to_time)))/60)
                differrence = to_time - from_time

                if task_id:
                    project_id = task_id.project_id
                    account_analytic.create({'name':record.description,'project_id':project_id.id,'task_id':task_id.id,'unit_amount':differrence})
                    task_id.active_task = False


