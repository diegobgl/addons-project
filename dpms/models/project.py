# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from openerp import tools
from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _name = 'dpms.project'
    _description = ' DPMS Project'
    _rec_name = 'title'
    code = fields.Char()
    title = fields.Char(required=True)
    owner_id = fields.Many2one('dpms.department')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string="Due Date")
    duration = fields.Integer(compute='compute_duration', store=True, string='Duration')
    projecttype_id = fields.Many2one('dpms.projecttype', required=True, string="Project Type")
    projecttype_title = fields.Char(related='projecttype_id.title', string="Project Type Title")
    status = fields.Selection(
        [('not started', 'Not Started'), ('on going', 'On Going'), ('suspended', 'Suspended'), ('closed', 'Closed'),
         ('pending', 'Pending')], string='Overall Status')
    budget = fields.Float(digits=(10, 2), string='Allocated Budget')
    spent_budget = fields.Float(compute='compute_spent_budget', store=True, string='Spent Budget')
    issue_ids = fields.One2many('dpms.issue', 'project_id')
    risk_ids = fields.One2many('dpms.risk', 'project_id')
    milestone_ids = fields.One2many('dpms.phase', 'project_id')
    issue_count = fields.Integer(compute='_onchange_issues', store=True, string='Issue Count')
    risk_count = fields.Integer(compute='_onchange_risk', store=True, string='Risk Count')
    progression_chart = fields.Char(compute='_onchange_progression', store=True)
    phase_count = fields.Integer(compute='compute_phase_count')
    phase_load = fields.Boolean(default=False)
    progression = fields.Float(compute='compute_progression', string="Overall Completion Progression %", store=True)
    projectmanager_id = fields.Many2one('dpms.employee', string='Project Manager')
    stakeholder_ids = fields.One2many('dpms.stakeholder', 'project_id')
    description = fields.Text(string='Description')
    planned_actions = fields.Text(string='Planned Actions')
    # priority = fields.Text(string='Priority')
    priority = fields.Selection([('mandatory', 'Mandatory'), ('nice to have', 'must do'), ('Must do', 'Nice to have')])
    # category = fields.Text(string='Project Category')
    category = fields.Selection(
        [('revenue ', 'Revenue'), ('cost efficiency', 'Cost efficiency'), ('process & systems', 'Process & Systems')],
        string='Project Category')
    ready = fields.Text(string='Ready By', default='Capex requirements\n \
Opex implication: opex to run, opex savings\n \
Resources requirements including estimate of IT resources\n \
Dependencies (ie what are pre requisite)\n \
')
    budget_resources = fields.Text(string='Budget & Resources')
    has_phases = fields.Boolean(compute='_has_phases', store=True)
    attachment_ids = fields.One2many('dpms.attachment', 'project_id')
    progression_text = fields.Char(compute='get_progression_text', store=True)
    user_id = fields.Many2one(related='projectmanager_id.user_id', string='User')
    programuser_id = fields.Many2one(related='program_id.user_id')
    program_id = fields.Many2one('dpms.program', string='Program')
    keyachievements = fields.Text(string='Key Achievements')
    current_status = fields.Text(string="Current Status")
    roadmap = fields.Text(string='Roadmap')
    delay = fields.Integer(compute='_compute_deplay',store=True)
    project_sponsor = fields.Many2one('dpms.employee',string='Project Sponsor')
    project_weight= fields.Float(digits=(10,2),default=0,string= 'Project Weight')
    planned_sites = fields.Integer(string='Planned Sites')
    offline_sites = fields.Integer(string="Offline Sites")
    onair_sites = fields.Integer(string="ON AIR Sites")
    accepted_sites = fields.Integer(string='Accepted Sites')

    @api.multi
    def write(self, vals):
        if vals.get('keyachievements'):
            self.env['dpms.changehistory'].create({'project_id': self.id, 'user_id': self._uid, 'field_name': 'Key Achievements','old_value': self.keyachievements, 'new_value': vals['keyachievements']})
        if vals.get('planned_actions'):
            self.env['dpms.changehistory'].create({'project_id': self.id, 'user_id': self._uid, 'field_name': 'Planned Actions','old_value': self.planned_actions, 'new_value': vals['planned_actions']})
        if vals.get('current_status'):
            self.env['dpms.changehistory'].create({'project_id': self.id, 'user_id': self._uid, 'field_name': 'Current Status','old_value': self.current_status, 'new_value': vals['current_status']})
        if vals.get('issue_ids'):
            self.env['dpms.changehistory'].create({'project_id': self.id, 'user_id': self._uid, 'field_name': 'Issues'})
        if vals.get('risk_ids'):
            self.env['dpms.changehistory'].create({'project_id': self.id, 'user_id': self._uid, 'field_name': 'Risks'})

        return super(Project, self).write(vals)


    @api.one
    @api.depends('end_date')
    def _compute_deplay(self):
        if self.end_date != False:
            today_date = datetime.now()
            due_date = datetime.strptime(self.end_date, tools.DEFAULT_SERVER_DATE_FORMAT)
            delta = today_date - due_date
            self.delay = delta.days
        else:
            self.delay= 0

    @api.one
    @api.depends('progression')
    def _onchange_progression(self):
        color = 'red'
        if self.progression > 0 and self.progression <=25:
            color = 'red'
        if self.progression > 25 and self.progression <=50:
            color = 'orange'
        if self.progression > 50  and self.progression <=75:
            color = 'yellow'
        if self.progression > 75 and self.progression <= 100:
            color = 'green'
        progress = '%.0f' % self.progression
        self.progression_chart = '<div style="background-color:'+str(color) +';height:28px;width:'+ str(progress) +'%"></div>'

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        if not vals.get('code'):
            sequence = self.env['ir.sequence'].get('dpms.project')
            vals['code'] = sequence
        return super(Project, self).create(vals)


    @api.one
    @api.depends('progression')
    def get_progression_text(self):
        self.progression_text = str(self.progression) + ' %'

    @api.one
    @api.depends('issue_ids')
    def _onchange_issues(self):
        result = 0
        for item in self.issue_ids:
            result = result + 1
        self.issue_count = result

    @api.one
    @api.depends('milestone_ids')
    def compute_progression(self):
        total = 0
        for phase in self.milestone_ids:
            if phase.weight != False and phase.progression != False:
                total = total + (phase.weight * phase.progression) / 100
        self.progression = total

    @api.one
    @api.depends('milestone_ids')
    def compute_spent_budget(self):
        total = 0
        for phase in self.milestone_ids:
            if phase.budget != False:
                total = total + phase.budget
        self.spent_budget = total

    @api.one
    @api.depends('milestone_ids')
    def compute_phase_count(self):
        count = 0
        for item in self.milestone_ids:
            count = count + 1
        self.phase_count = count

    @api.one
    @api.depends('milestone_ids')
    def _has_phases(self):
        if self.milestone_ids != False:
            self.has_phases = len(self.milestone_ids)
        else:
            self.has_phases = 0

    @api.one
    @api.depends('risk_ids')
    def _onchange_risk(self):
        result = 0
        for item in self.risk_ids:
            result = result + 1
        self.risk_count = result

    @api.one
    @api.depends('start_date','end_date')
    def compute_duration(self):
        if self.start_date !=False and self.end_date !=False:
            end = self.end_date.split(' ')[0]
            start = self.start_date.split(' ')[0]
            end_date = datetime.strptime(end, '%Y-%m-%d')
            start_date = datetime.strptime(start, '%Y-%m-%d')
            self.duration = (end_date - start_date).days

    @api.one
    def load_phases(self):
        _logger.error('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        # self.env['dpms.phase'].create({'title': 'Hello world', 'weight': 25.00})
        current_project_id = self.id
        if self.projecttype_id != False:
            projecttype_id = self.projecttype_id.id
            phases = self.env['dpms.projecttypephase'].search([('projecttype_id', '=', projecttype_id)])
            for item in phases:
                _logger.error(item.weight)
                self.env['dpms.phase'].create(
                    {'project_id': current_project_id, 'title': item.name, 'weight': item.weight})
        _logger.error('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    @api.multi
    def export_excel(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/dpms/project/%d' % (self.id),
            'target': 'self',
        }

    @api.multi
    def export_planning_excel(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/dpms/projectplanning/%d' % (self.id),
            'target': 'self',
        }


class Issue(models.Model):
    _name = 'dpms.issue'
    _description = 'DPMS Issue'
    _rec_name = 'title'
    project_id = fields.Many2one('dpms.project')
    title = fields.Char(string='Title', required=True)
    impact = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
                              string='Impact')
    action = fields.Text(string='Action Plan')
    resolution_date = fields.Date(string='Resolution Date')
    owner_id = fields.Many2one('dpms.department', string='Owner')
    status = fields.Selection([('solved', 'Solved'), ('pending', 'Pending')], default='pending', string='Status')


class Risk(models.Model):
    _name = 'dpms.risk'
    _description = 'DPMS Risk'
    _rec_name = 'title'
    title = fields.Char(string='Title', required=True)
    impact = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
                              string='Impact')
    mitigation = fields.Text(string='Action Plan')
    resolution_date = fields.Date(string='Resolution Date')
    owner_id = fields.Many2one('dpms.department', string='Owner')
    status = fields.Selection([('solved', 'Solved'), ('pending', 'Pending')], default='pending', string='Status')
    project_id = fields.Many2one('dpms.project')


class Stakeholder(models.Model):
    _name = 'dpms.stakeholder'
    _description = 'DPMS Stakeholder'
    department_id = fields.Many2one('dpms.department', string='Department', required=True)
    project_id = fields.Many2one('dpms.project')


class Attachment(models.Model):
    _name = 'dpms.attachment'
    _description = 'DPMS Attachment'
    title = fields.Char(string='Title', help='Relevant title of the uploaded document')
    filename = fields.Char()
    project_id = fields.Many2one('dpms.project')
    data = fields.Binary("File", help='Select a file to upload')
    description = fields.Char(string='Description')
    phase_id = fields.Many2one('dpms.phase',string='Phase')
