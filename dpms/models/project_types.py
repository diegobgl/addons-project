# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import  Warning
import logging

_logger = logging.getLogger(__name__)

class ProjectType(models.Model):
    _name = 'dpms.projecttype'
    _description= 'DPMS prpject type'
    _rec_name= 'title'
    title = fields.Char(required=True)
    description = fields.Text()
    phase_ids = fields.One2many('dpms.projecttypephase','projecttype_id')
    phase_count = fields.Integer(compute='_get_phases_count',store=True,string='Phases Count')

    @api.one
    @api.depends('phase_ids')
    def _get_phases_count(self):
        if self.phase_ids == False:
            self.phase_count = 0
        else:
            self.phase_count= len(self.phase_ids)

    # @api.multi
    # def write(self,vals):
    #     a = vals['phase_ids']
    #     total = 0
    #     for item in a:
    #         if item[2] != False:
    #             if item[2].get('weight') != None:
    #                 total = total + item[2]['weight']
    #             else:
    #                 item2 = self.env['dpms.projecttypephase'].browse(item[1])
    #                 total = total + item2.weight
    #         else:
    #             item2 = self.env['dpms.projecttypephase'].browse(item[1])
    #             total = total + item2.weight
    #     _logger.error('total: ' + str(total))
    #     if total > 100:
    #         raise Warning('Error, total weight is greater than 100% !')




class ProjectTypePhase(models.Model):
    _name = 'dpms.projecttypephase'
    _description = 'DPMS Project Type Phase'
    name = fields.Char(required=True)
    projecttype_id = fields.Many2one('dpms.projecttype')
    weight = fields.Float(digits=(4,2), string='Weight',default= 0)

