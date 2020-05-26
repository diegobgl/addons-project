# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Delivery(models.Model):
    _name = 'dpms.delivery'
    _description = 'DPMS Delivery'
    title = fields.Char()
    filename = fields.Char()
    phase_id = fields.Many2one('dpms.phase')
    data = fields.Binary("File",help='Select a file to upload')