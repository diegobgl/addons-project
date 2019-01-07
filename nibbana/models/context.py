from .utils import generate_uid
from odoo import fields, models, api, _


class Context(models.Model):
    _name = 'nibbana.context'
    _order = 'name'

    name = fields.Char(required=True)
    description = fields.Text()
    tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='context')
    task_count = fields.Integer(string=_('Tasks'), compute='_get_task_count')
    projects = fields.One2many(comodel_name='nibbana.project', inverse_name='context')
    project_count = fields.Integer(compute='_get_project_count',
                                   string=_('Projects'))
    uid = fields.Char(required=True, index=True, size=32,
                      default=generate_uid)

    _sql_constraints = [
        ('uid_uniq', 'UNIQUE(uid)', _('The uid must be unique !')),
    ]


    @api.one
    def _get_project_count(self):
        self.project_count = self.env['nibbana.project'].search_count([
            ('context', '=', self.id)])

    @api.one
    def _get_task_count(self):
        self.task_count = self.env['nibbana.task'].search_count([
            ('context', '=', self.id), ('state','not in',['Done','Cancelled'])])


    @api.one
    def _get_reference_count(self):
        self.reference_count = self.env['nibbana.reference'].search_count([
            ('context', '=', self.id)])


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):        
        default = dict(default or {})
        default.update({'uid': generate_uid(self)})
        return super(Context, self).copy(default)
