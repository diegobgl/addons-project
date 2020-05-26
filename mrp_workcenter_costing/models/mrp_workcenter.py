# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    costs_hour = fields.Float(string='Direct Cost Rate per hour', default="0.0")
    costs_dir_analytic_account_id = fields.Many2one('account.analytic.account', string="Direct Cost Analytic Account")
    costs_dir_account_id = fields.Many2one('account.account', string="Direct Cost Account")
    #journal_id = fields.Many2one('account.journal')

    costs_hour_fixed = fields.Float(string='Fixed Direct Cost Rate per hour', default="0.0")
    costs_fixed_analytic_account_id = fields.Many2one('account.analytic.account', string="Fixed Direct Cost Analytic Account")

    costs_overheads_fixed_percentage = fields.Float(string='Fixed OVH Costs %', default="0.0")
    costs_overheads_fixed_analytic_account_id = fields.Many2one('account.analytic.account', string="Fixed OVH Costs Analytic Account")
    costs_overheads_variable_percentage = fields.Float(string='Variable OVH Costs %', default="0.0")
    costs_overheads_variable_analytic_account_id = fields.Many2one('account.analytic.account', string="Variable OVH Costs Analytic Account")

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id.id) 
