# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class TemplateDocument(models.Model):
    _name = 'dpms.documenttemplate'
    _description = 'DPMS Document template'
    title =fields.Char(string='Title')
    description = fields.Text(string='Description')
    filename = fields.Char()
    data = fields.Binary("File", help='Select a file to upload')