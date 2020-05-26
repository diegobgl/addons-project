#-*- coding:utf-8 -*-

from odoo import models, fields, api

class ProjectExportWizard(models.TransientModel):
    _name  ='dpms.projectexportwizard'
    _description = 'DPMS Project Export Wizard Model'

    def _default_session(self):
        return self.env['dpms.project'].browse(self._context.get('active_id'))

    project_id = fields.Many2one('dpms.project',string="Project", required=True, default=_default_session)

    @api.multi
    def export_project(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/details/employee/%s' % (self.project_id.id)
        }