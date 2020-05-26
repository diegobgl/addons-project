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

class Project(models.Model):
    _inherit = "project.project"

    skills_ids = fields.Many2many('project.tech.skill', string='Skills', help='Select Skills which are required for project')

    #This Function is used to Find and Display Employee having the same Skill set as Project.
    def check_skilled_resources(self):
        if self.id:
            template_id = self.env.ref('abs_project_skill_matching.view_skilled_resources_tree').id
            skills = []
            employees = []
            for record in self:
                skill_ids = record.skills_ids
            for skill in skill_ids:
                skills.append(skill.id)
            employee_ids = self.env['hr.employee'].search([('skills_ids', 'in', skills)])
            for emp in employee_ids:
                employees.append(emp.id)
            return {
                    'name': _('List of Skilled Resources'),
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'res_model': 'hr.employee',
                    'type': 'ir.actions.act_window',
                    'view_id': template_id,
                    'views': [(self.env.ref('abs_project_skill_matching.view_skilled_resources_tree').id, 'tree')],
                    'domain': [('id','in',employees)]}

 


