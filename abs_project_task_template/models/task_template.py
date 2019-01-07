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
from odoo import api,fields,models,_

#New Class Is Created For Task Template.
class TaskTemplate(models.Model):
    _name='project.task.template'

    name = fields.Char(string='Task Title', track_visibility='always', required=True, help=" The Title Of Task")
    user_id = fields.Many2one('res.users', string='Assigned to', index=True, track_visibility='always', help="Many2one Field Related To res user")
    date_deadline = fields.Date(string='Deadline', copy=False, help="Date Field For Deadline")
    description = fields.Html(string='Description', help="Html Field For Description")
    active = fields.Boolean(default=True, help="Boolean Field For Task Status")


#Class Is Extended For Add New Feature Of Task Template.
class Project(models.Model):
    _inherit = 'project.project'

    use_task_template = fields.Boolean(string="Use Active Task Templates", help="Use Task Templates for creating Tasks of the Project")
   
    #Create Method Override To Add Task Template At The Time Of Project Creation.
    @api.model
    def create(self,vals):
        variable=super(Project,self).create(vals)
        if vals.get('use_task_template'):
            template_id = self.env['project.task.template'].search([('active','=',True)])
            if template_id:
                 for template in template_id: 
                     tasktemplate={}
                     tasktemplate['name']=template.name
                     tasktemplate['user_id']=template.user_id.id
                     tasktemplate['date_deadline']=template.date_deadline
                     tasktemplate['description']=template.description
                     tasktemplate['project_id']=variable.id
                     self.env['project.task'].create(tasktemplate)
        return variable 




  
