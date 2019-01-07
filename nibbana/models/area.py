import re
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from .utils import generate_uid


class Area(models.Model):
    _name = 'nibbana.area'
    _order = 'name'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    project_count = fields.Integer(compute='_get_project_count',
                                   string=_('Projects'))
    task_count = fields.Integer(compute='_get_task_count',
                                   string=_('Tasks'))
    reference_count = fields.Integer(compute='_get_reference_count',
                                     string=_('References'))
    active_project_limit = fields.Integer(default=3)
    color = fields.Char(size=7, default='#FFFFFF')
    uid = fields.Char(required=True, index=True, size=32,
                      default=generate_uid)


    _sql_constraints = [
        ('uid_uniq', 'UNIQUE(uid)', _('The uid must be unique !')),
    ]

    @api.one
    def _get_project_count(self):
        self.project_count = self.env['nibbana.project'].search_count([
            ('area', '=', self.id)])


    @api.one
    def _get_task_count(self):
        self.task_count = self.env['nibbana.task'].search_count([
            ('area', '=', self.id),('state','not in',['Done','Cancelled'])])


    @api.one
    def _get_reference_count(self):
        self.reference_count = self.env['nibbana.reference'].search_count([
            ('area', '=', self.id)])


    @api.multi
    def toggle_active(self):
        for self in self:
            self.active = not self.active


    @api.constrains('color')
    def _check_color(self):
        if self.color:
            if len(self.color) !=7 or self.color[0] != '#' or \
                    not re.search('[0-9A-Z]{6}', self.color[1:].upper()):
                raise ValidationError(_('Color must be in format of #AABBCC!'))


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):        
        default = dict(default or {})
        default.update({'uid': generate_uid(self)})
        return super(Area, self).copy(default)
