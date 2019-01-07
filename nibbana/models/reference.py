import logging
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from .utils import generate_uid

logger = logging.getLogger(__name__)



class ReferenceArea(models.Model):
    _name = 'nibbana.area_reference'
    
    reference_id = fields.Many2one('nibbana.reference', required=True, ondelete='cascade')
    area_id = fields.Many2one('nibbana.area', required=True, ondelete='cascade')



class Reference(models.Model):
    _name = 'nibbana.reference'
    _order = 'sequence,name'
    _description = _('Reference')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    content = fields.Html(required=True)
    project = fields.Many2one(comodel_name='nibbana.project', ondelete='cascade')
    project_state = fields.Selection(related='project.state', readonly=True)
    area = fields.Many2one(comodel_name='nibbana.area',
                           compute='_get_area', inverse='_set_area',
                           search='_search_area')
    area_color = fields.Char(compute=lambda self: self._get_area_color())
    uid = fields.Char(required=True, index=True, size=32,
                      default=generate_uid)
    contacts = fields.Many2many('res.partner')


    @api.model
    def create(self, vals):
        res = super(Reference, self).create(vals)
        self.env['nibbana.timeline'].timeline_create_event(res)
        return res


    @api.multi
    def unlink(self):
        for rec in self:
            self.env['nibbana.timeline'].timeline_unlink_event(rec)
        return super(Reference, self).unlink()


    @api.multi
    def write(self, vals):
        if vals.get('name') or vals.get('content'): 
            for rec in self:
                self.env['nibbana.timeline'].timeline_update_event(rec, vals, 
                        ['name', 'content', 'project'])
        return super(Reference, self).write(vals)


    @api.multi
    def _get_area(self):
        for self in self:
            if not self.project:
                area = self.env['nibbana.area_reference'].search([
                        ('create_uid','=',self.env.user.id),
                        ('reference_id','=', self.id)], limit=1)
                self.area = area.area_id if area else False
            else:
                self.area = self.project.area


    @api.multi
    def _set_area(self):
        for self in self:
            if not self.area:
                continue            
            area = self.env['nibbana.area_reference'].search([
                    ('create_uid','=',self.env.user.id),
                    ('reference_id','=', self.id)])
            if not area:
                self.env['nibbana.area_reference'].create({
                    'reference_id': self.id,
                    'area_id': self.area.id
                })
            else:
                area.area_id = self.area.id


    def _search_area(self, operator, value):
        if operator == 'ilike':
            area = self.env['nibbana.area'].search([
                    ('create_uid','=',self.env.user.id),
                    ('name', 'ilike', value)])
            if not area:
                return [('id','=', False)]
            references = self.env['nibbana.area_reference'].search([
                ('create_uid','=', self.env.user.id),
                ('area_id','in',[k.id for k in area])])
            return [('id','in', [k.reference_id.id for k in references])]
        
        elif operator in ['in', '=']:
            if not type(value) is list:
                value = [value]
            references_area_ids = [k.reference_id.id for k in self.env[
                                    'nibbana.area_reference'].search([
                        ('create_uid','=',self.env.user.id),
                        ('area_id', 'in', value)])]            
            return [('id', 'in', references_area_ids)]
        else:
            raise ValidationError(_('Search area by {} not implemented!').format(operator))


    @api.multi
    def _get_area_color(self):
        for self in self:
            self.area_color = self.area.color


    @api.onchange('project')
    def set_area_by_project(self):
        if self.project:
            self.area = self.project.area


    @api.onchange('area')
    def set_project(self):
        # Check that currenly selected project is not from another area
        if self.area:
            if self.project and self.project.area != self.area:
                self.project = False
            projects_area_ids = [k.project_id.id for k in self.env[
                                    'nibbana.area_project'].search([
                        ('create_uid','=',self.env.user.id),
                        ('area_id', '=', self.area.id)])]
            return {
                'domain': {'project': [('id','in', projects_area_ids)]},
            }
        else:
            return {
                'domain': {'project': []},
            }


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):        
        default = dict(default or {})
        default.update({'uid': generate_uid(self)})
        return super(Reference, self).copy(default)

