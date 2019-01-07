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

class ProjectTask(models.Model):
    _inherit = "project.task"
 
    stage_instructions = fields.Text(string="Stage Instructions",readonly=True,help='This field shows the instuctions, when click on the status button.')

    #This function will get satge_id and its instruction.
    def write(self, vals):
        for record in self:
            if vals.get('stage_id',False):
                temp = vals['stage_id']
                temp = self.env['project.task.type'].browse(temp).stage_instructions
                vals['stage_instructions']=temp
            return super(ProjectTask, self).write(vals)
        
