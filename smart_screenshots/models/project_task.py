from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    screenshot_problem_ids = fields.One2many(
        comodel_name='project.task.screenshot',
        inverse_name='problem_task_id',
        string='Problem Screenshot')
    screenshot_solution_ids = fields.One2many(
        comodel_name='project.task.screenshot',
        inverse_name='solution_task_id',
        string='Solution Screenshot')

    @api.model
    def get_last_task_id(self):
        last_task = self.env['project.task'].search([], limit=1, order='id desc')
        if last_task:
            return {'task_id': last_task.id}
        return {'task_id': False}

    @api.multi
    def show_screenshot_settings(self):
        action = self.env.ref('smart_screenshots.project_screenshot_settings_action').read()[0]
        action['domain'] = [('project_id', '=', self.project_id.id), ('user_id', '=', self.env.user.id)]
        action['context'] = {'default_project_id': self.project_id.id}
        return action

