from odoo import fields, models, api
from urllib.parse import urlparse
import requests


class ProjectTaskScreenshot(models.Model):
    _name = 'project.task.screenshot'
    _description = 'ProjectTaskScreenshot'

    name = fields.Char(
        string='Name')
    problem_task_id = fields.Many2one(
        comodel_name='project.task',
        ondelete='cascade',
        string='Task')
    solution_task_id = fields.Many2one(
        comodel_name='project.task',
        ondelete='cascade',
        string='Task')
    project_id = fields.Many2one(
        comodel_name='project.project',
        compute='_compute_project_id',
        string='Project')
    image = fields.Binary(
        string="Image",
        required=True)
    type = fields.Selection(
        string='Type',
        selection=[('problem', 'Problem'),
                   ('solution', 'Solution'), ],
        default='problem')
    source_url = fields.Char(
        string='Source url')
    replacement_url = fields.Char(
        string='Replacement url',
        compute='_compute_replacement_url')
    share_url = fields.Char(
        string='Share url')
    attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
        delete='cascade',
        string='Attachment')

    @api.depends('problem_task_id', 'solution_task_id')
    def _compute_project_id(self):
        for rec in self:
            if rec.problem_task_id:
                rec.project_id = rec.problem_task_id.project_id.id
            elif rec.solution_task_id:
                rec.project_id = rec.solution_task_id.project_id.id
            else:
                rec.project_id = False

    @api.depends('source_url')
    def _compute_replacement_url(self):
        for rec in self.filtered('source_url'):
            source = urlparse(rec.source_url)
            domain = self.env['project.screenshot.settings.domain'].search([('name', '=', source.netloc)], limit=1)
            if domain:
                settings = self.env['project.screenshot.settings'].search([('project_id', '=', rec.project_id.id),
                                                                           ('user_id', '=', self.env.user.id),
                                                                           ('source_domain_id', '=', domain.id)],
                                                                          limit=1)
                if settings:
                    rec.replacement_url = source._replace(netloc=settings.replacement_domain_id.name).geturl()
            else:
                rec.replacement_url = False

    @api.multi
    def share_screenshot(self):
        self.ensure_one()
        if not self.share_url:
            url = "https://www.openscreenshot.com/upload3.asp"
            data = {
                'type': 'png',
                'title': 'TITLE',
                'description': 'description',
                'imageUrl': self.source_url,
                'option': '9ea4da4aca31b28e4faaf52c831b9024e81c1bbcd67b8784f19d67a8055b69d5',
                'data': "data:image/png;base64," + self.image.decode('utf8'),
            }
            r = requests.post(url, data=data)
            self.share_url = r.text
        return {
            "type": "ir.actions.act_url",
            "url": self.share_url,
            "target": "new",
        }

    @api.multi
    def open_replacement_domain(self):
        if self.replacement_url:
            return {
                "type": "ir.actions.act_url",
                "url": self.replacement_url,
                "target": "new",
            }

        domain_str = urlparse(self.source_url).netloc
        domain = self.env['project.screenshot.settings.domain'].search([('name', '=', domain_str)], limit=1)
        if not domain:
            domain = self.env['project.screenshot.settings.domain'].create({'name': domain_str})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Domain Mapping',
            'res_model': 'project.screenshot.settings',
            'domain': [('project_id', '=', self.project_id.id)],
            'context': {'default_project_id': self.project_id.id,
                        'default_source_domain_id': domain.id, },
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
        }
