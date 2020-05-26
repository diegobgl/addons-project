# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from odoo import exceptions
_logger = logging.getLogger(__name__)

class Phase(models.Model):
    _name= 'dpms.phase'
    _description = 'DPMS Phase'
    _rec_name = 'title'
    project_id = fields.Many2one('dpms.project',string='Project')
    owner_id = fields.Many2one('dpms.employee', string='Owner')
    title = fields.Char(string='Title',required=True)
    status = fields.Selection([('not started', 'Not Started'), ('on going', 'On Going'), ('suspended', 'Suspended'), ('closed', 'Closed'),('pending', 'Pending')],default='not started', string='Overall Status')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    budget = fields.Float(digits=(10,2),default=0,string= 'Budget')
    weight =  fields.Float(digits=(4,2),string='Weight',help='Percentage of the phase in the whole project progression')
    progression = fields.Float(digits=(4,2),string='Progression',help='Percentage of the progression in the current phase')
    Description = fields.Html(string='Description',help='Provide an overview of this phase and objectives')
    parent_id = fields.Many2one('dpms.phase')
    delivery_ids = fields.One2many('dpms.delivery','phase_id')
    #predecessor_ids = fields.One2many('dpms.predecessor','origin_id')
    responsibility_ids =fields.One2many('dpms.responsability','phase_id')

    @api.onchange('weight')
    def _weight_change(self):
        total = 0
        for item in self.project_id.milestone_ids:

            if isinstance(item.id, int):
                if item.id != self._origin.id:
                    total = total + item.weight
                else:
                    total = total + self.weight
        if total > 100 or total < 0:
            return { 'warning' :{'title' : 'Project Weight Error','message' : 'Total Phase Weight cannot be exceed 100% !'}}



class Responsability(models.Model):
    _name = 'dpms.responsability'
    _description = 'DPMS Responsability'
    phase_id = fields.Many2one('dpms.phase')
    department_id = fields.Many2one('dpms.department',string='Department',required=True)
    responsibility = fields.Boolean(string='Responsible')
    accountable = fields.Boolean(string='Accountable')
    consulted = fields.Boolean(string='Consulted')
    informed = fields.Boolean(string='Informed')
    resources = fields.Integer(string='Affected Resources')





# class PhasePredecessor(models.Model):
#     _name = 'dpms.predecessor'
#     _description = 'DPMS Predecessor'
#     origin_id = fields.Many2one('dpms.phase')
#     phase_id = fields.Many2one('dpms.phase',required=True)

