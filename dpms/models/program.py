# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class Program(models.Model):
    _name= 'dpms.program'
    _description = 'DPMS Program'
    _rec_name = 'title'
    title = fields.Char(required=True, string='Title')
    project_ids = fields.One2many('dpms.project','program_id')
    start_date  =fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date')
    budget = fields.Float(digits=(15,2),string='Overall Budget')
    owner_id = fields.Many2one('dpms.department')
    progression = fields.Float(compute='_compute_progression',store=True, string='Progression (%)')
    description = fields.Text(string='Description')
    budget_resources = fields.Text(string='Budget & Resources')
    ready = fields.Text(string='Ready By', default='Capex requirements\n \
    Opex implication: opex to run, opex savings\n \
    Resources requirements including estimate of IT resources\n \
    Dependencies (ie what are pre requisite)\n \
    ')
    risk_ids = fields.One2many('dpms.programrisk','program_id')
    issue_ids = fields.One2many('dpms.programissue', 'program_id')
    risk_count = fields.Integer(compute='_count_risk',store=True)
    issue_count = fields.Integer(compute='_count_issue', store=True)
    spent_budget = fields.Float(compute='_compute_spent_budget',store=True,string='Spent Budget')
    programmanager_id =  fields.Many2one('dpms.programmanager',string='Program Manager')
    user_id = fields.Many2one(related='programmanager_id.user_id', string='User')

    @api.one
    @api.depends('project_ids')
    def _compute_spent_budget(self):
        total = 0
        if self.project_ids != False:
            for item in self.project_ids:
                total = total + item.spent_budget
            self.spent_budget = total

    @api.one
    @api.depends('issue_ids')
    def _count_issue(self):
        if self.issue_ids != False:
            self.issue_count = len(self.issue_ids)

    @api.one
    @api.depends('risk_ids')
    def _count_risk(self):
        if self.risk_ids != False:
            self.risk_count = len(self.risk_ids)


    @api.one
    @api.depends('project_ids')
    def _compute_progression(self):
        count = len(self.project_ids)
        if count > 0:
            total = 0
            for item in self.project_ids:
                total = total + item.progression
            self.progression = total / count


class ProgramRisk(models.Model):
    _name = 'dpms.programrisk'
    _description = 'DPMS Program Risk'
    _rec_name = 'title'
    title = fields.Char(string='Title', required=True)
    impact = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],string='Impact')
    mitigation = fields.Text(string='Action Plan')
    resolution_date = fields.Date(string='Resolution Date')
    owner_id = fields.Many2one('dpms.department', string='Owner')
    status = fields.Selection([('solved', 'Solved'), ('pending', 'Pending')], default='pending', string='Status')
    program_id = fields.Many2one('dpms.program')


class ProgramIssue(models.Model):
    _name = 'dpms.programissue'
    _description = 'DPMS Program Issue'
    _rec_name = 'title'
    program_id = fields.Many2one('dpms.program')
    title = fields.Char(string='Title', required=True)
    impact = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],string='Impact')
    action = fields.Text(string='Action Plan')
    resolution_date = fields.Date(string='Resolution Date')
    owner_id = fields.Many2one('dpms.department', string='Owner')
    status = fields.Selection([('solved', 'Solved'), ('pending', 'Pending')], default='pending', string='Status')


