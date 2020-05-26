from odoo import models, fields, api, _


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    set_default = fields.Boolean('Default?')


class ProjectDefault(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        rtn = super(ProjectDefault, self).create(vals)
        stage_obj = self.env['project.task.type']
        stage_ids = stage_obj.search([('set_default', '=', True)])

        project_ids = tuple([x.id for x in rtn])
        for stage in stage_ids:
            stage.write({'project_ids': [(4, project_ids, 0)]})

        return rtn
