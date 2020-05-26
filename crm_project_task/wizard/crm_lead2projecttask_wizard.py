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


class CrmLeadToProjectTaskWizard(models.TransientModel):
    _name = "crm.lead2projecttask.wizard"
    _inherit = 'crm.partner.binding'

    @api.model
    def default_get(self, fields):
        result = super(CrmLeadToProjectTaskWizard, self).default_get(fields)
        lead_id = self.env.context.get('active_id')
        if lead_id:
            result['lead_id'] = lead_id
        return result

    lead_id = fields.Many2one('crm.lead', string='Lead',
                              domain=[('type', '=', 'lead')])
    project_id = fields.Many2one('project.project', string='Project')
    asigned_id = fields.Many2one('res.users', string="Assigned to",
                                 required=False)
    date_deadline = fields.Date(string="Deadline", required=False)

    @api.multi
    def action_lead_to_project_task(self):
        self.ensure_one()

        lead = self.lead_id
        partner_id = self._find_matching_partner()
        if not partner_id and (lead.partner_name or lead.contact_name):
            partner_id = lead.handle_partner_assignation()[lead.id]

        vals = {
            "name": lead.name,
            "description": lead.description,
            "email_from": lead.email_from,
            "project_id": self.project_id.id,
            "partner_id": partner_id,
            "user_id": self.asigned_id.id,
            "date_deadline": self.date_deadline,
            "opportunity_id": lead.id
        }
        task = self.env['project.task'].create(vals)

        lead.message_change_thread(task)

        attachments = self.env['ir.attachment'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id)])
        attachments.write({'res_model': 'project.task', 'res_id': task.id})

        # lead.write({'active': False})

        view = self.env.ref('project.view_task_form2')
        return {
            'name': 'Task created',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'res_id': task.id,
            'context': self.env.context
        }
