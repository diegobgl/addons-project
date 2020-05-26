# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employee(models.Model):
    _name = 'dpms.employee'
    name = fields.Char(string= 'Name',required=True)
    title = fields.Char(string='Title')
    description =fields.Text(string='Description')
    department_id = fields.Many2one('dpms.department', string= 'Department')
    user_id = fields.Many2one('res.users',string='User')


class Department(models.Model):
    _name= 'dpms.department'
    _description = 'DPMS Department'
    name = fields.Char(required=True, string='Name')
    description = fields.Char(string="Description")


class ProgramManager(models.Model):
    _name = 'dpms.programmanager'
    _description = 'DPMS Program Manager'
    name = fields.Char(string='Name',required=True)
    title = fields.Char(string='Title')
    department_id = fields.Many2one('dpms.department',string='Department')
    user_id = fields.Many2one('res.users',string='User')





