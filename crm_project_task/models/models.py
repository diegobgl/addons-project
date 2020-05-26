#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################
#
# Difusión Visual Interactivo S.L.
# Copyright (C) Difusión Visual Interactivo S.L.
# all rights reserved
# http://difusionvisual.com
# contacto@difusionvisual.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
from odoo import api, fields, models


class LeadinTask(models.Model):
    _inherit = 'project.task'

    opportunity_id = fields.Many2one("crm.lead", string="Opportunity", required=False, )


class LeadTaskCount(models.Model):
    _inherit = 'crm.lead'

    taskcount = fields.Integer(string="Task", required=False, compute='_get_task_count')
    project_id = fields.Many2one("project.project", string="Project", required=False, )

    @api.one
    @api.depends('partner_id')
    def _get_task_count(self):
        domain = [('opportunity_id', '=', self.id)]
        count = self.env['project.task'].search_count(domain)
        self.taskcount = count


class LeadTaskCountProject(models.Model):
    _inherit = 'project.project'

    leadcount = fields.Integer(string="Lead", required=False, compute='_get_lead_count')

    @api.one
    @api.depends('partner_id')
    def _get_lead_count(self):
        domain = [('project_id', '=', self.id)]
        count = self.env['crm.lead'].search_count(domain)
        self.leadcount = count
