# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from openerp import tools
import logging

_logger = logging.getLogger(__name__)

class ChangeHistory(models.Model):
    _name = 'dpms.changehistory'
    _description = 'DPMS Change History'
    _order = 'date desc'
    user_id = fields.Many2one('res.users',string='User')
    project_id = fields.Many2one('dpms.project',string='Project')
    date = fields.Datetime(string='Date',default=lambda self: fields.datetime.now())
    field_name = fields.Char(string='Field Name')
    old_value = fields.Char(string='Old Value')
    new_value = fields.Char(string='New Value')