from datetime import datetime
from .utils import generate_uid
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, MissingError
from odoo.osv import expression
import logging
from .utils import increment_metric, decrement_metric

logger = logging.getLogger(__name__)


STATES = (
        ('Active', _('Active')),
        ('Inactive', _('Inactive')),        
        ('Waiting', _('Waiting')),
        ('Scheduled', _('Scheduled')),
        ('Done', _('Done')),        
        ('Cancelled', _('Cancelled')),
    )



class Project(models.Model):
    _name = 'nibbana.project'
    _description = _('Project')
    _rec_name = 'name'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True)
    description = fields.Text()
    note = fields.Html()
    area = fields.Many2one(comodel_name='nibbana.area',
                           compute='_get_area', inverse='_set_area',
                           search='_search_area')
    area_color = fields.Char(compute=lambda self: self._get_area_color())
    area_list = fields.Char(compute='_area_list', string=_('Area'))
    context = fields.Many2many(comodel_name='nibbana.context',
                               compute='_get_context', inverse='_set_context',
                               search='_search_context')    
    context_list = fields.Char(compute='_context_list', string=_('Context'))
    has_context = fields.Boolean(compute='_has_context', store=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=STATES, index=True, default='Active')
    schedule_start_date = fields.Date()
    # Add state copy for status bar as we cannot have one field twice
    state_changed = fields.Datetime(string=_('Changed'),
                                    default=fields.Datetime.now)
    state_change_count = fields.Integer(default=0, string=_('Changes'))
    open_task_count = fields.Integer(compute='_open_task_count')
    closed_task_count = fields.Integer(compute='_closed_task_count')

    tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project')
    today_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                  context={'active_test': False},
                                  domain=[('state','=','Today')])
    tomorrow_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                  context={'active_test': False},
                                  domain=[('state','=','Tomorrow')])
    next_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                  context={'active_test': False},
                                  domain=[('state','=','Next')])
    someday_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                    context={'active_test': False},
                                    domain=[('state','=','Someday')])
    waiting_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                    context={'active_test': False},
                                    domain=[('state','=','Waiting')])
    scheduled_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                      context={'active_test': False},
                                      domain=[('state','=','Scheduled')])
    done_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                 context={'active_test': False},
                                  domain=[('state','=','Done')])
    cancelled_tasks = fields.One2many(comodel_name='nibbana.task', inverse_name='project',
                                      context={'active_test': False},
                                      domain=[('state','=','Cancelled')])
    references = fields.One2many(comodel_name='nibbana.reference', inverse_name='project')
    reference_count = fields.Integer(compute='_reference_count')
    focus = fields.Selection(selection=(
        ('0', _('Non-focused')),
        ('1', _('Focused'))), default='0')
    uid = fields.Char(required=True, index=True, size=32,
                  default=generate_uid)
    contacts = fields.Many2many('res.partner')

    _sql_constraints = [
        ('uid_uniq', 'UNIQUE(uid)', _('The uid must be unique !')),
    ]


    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)
        increment_metric(self, name = _('Projects'), code = 'projects_created')
        self.env['nibbana.timeline'].timeline_create_event(res)
        return res


    @api.multi
    def unlink(self):
        for rec in self:
            self.env['nibbana.timeline'].timeline_unlink_event(rec)
        return super(Project, self).unlink()

    @api.multi
    def write(self, vals): 
        for rec in self:
            if not vals.get('state_change_count') and ('state' in vals or 'focus' in vals):
                vals['state_change_count'] = rec.state_change_count + 1
                vals['state_changed'] = datetime.now()
            if vals.get('state') and vals['state'] != 'Scheduled':
                vals['schedule_start_date'] = False
            # State changes
            if vals.get('state'):
                # Do metrics
                increment_metric(rec, code='projects_changed', name=_('Projects'))
                if vals['state'] == 'Done' and rec.state != 'Done':
                    # Project set to Done
                    increment_metric(rec, code='projects_done', name=_('Projects'))
                elif vals['state'] != 'Done' and rec.state == 'Done':
                    decrement_metric(rec, code='projects_done', name=_('Projects'))
                # Archive 
                if vals['state'] in ['Done', 'Cancelled']:
                    vals['active'] = False                
                    rec.mapped('tasks').write({'active': False})
                    rec.mapped('references').write({'active': False})
                else:
                    vals['active'] = True
                    for t in rec.with_context(active_test=False).mapped('tasks'):
                        if t.state not in ['Done', 'Cancelled']:
                            t.write({'active': True})
                    rec.with_context(active_test=False).mapped('references').write(
                                                            {'active': True})
            self.env['nibbana.timeline'].timeline_update_event(rec, vals,
                            ['state', 'name', 'note', 'description', 'focus'])
        super(Project, self).write(vals)
        return True


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):        
        default = dict(default or {})
        default.update({'uid': generate_uid(self)})
        return super(Project, self).copy(default)


    def _read_group_fill_results(self, domain, groupby,
                                     remaining_groupbys, aggregated_fields,
                                     count_field, read_group_result,
                                     read_group_order=None):
            if groupby == 'state':
                result_states = {}
                for rec in read_group_result:
                        result_states[rec['state']] = rec

                results = []
                for state, _ in STATES:
                    if state in result_states:
                        results.append(result_states[state])
                    else:
                        results.append({'state': state, 'state_count': 0, 
                                       '__domain': [(u'state', '=', state)]})
                # Add fold info
                for result in results:
                    if result['state'] in ['Done', 'Cancelled']:
                        result['__fold'] = True
                return results

            else:
                return super(Project, self)._read_group_fill_results(
            domain, groupby, remaining_groupbys, aggregated_fields,
            count_field, read_group_result, read_group_order)





    @api.one
    @api.constrains('schedule_start_date')
    def _check_schedule_start_date(self):
        if self.schedule_start_date and self.schedule_start_date <= fields.Date.today():
            raise ValidationError(_('You should set a future date!'))


    @api.one
    @api.constrains('state')
    def check_limits(self):
        if self.area and self.state == 'Active':
            active_projects_count = self.env['nibbana.project'].search_count(
                [('area','=',self.area.id),('state','=','Active')])
            if active_projects_count > self.area.active_project_limit:
                raise ValidationError(_("Area's projects limit has been reached!"))


    @api.multi
    def set_state(self, state):
        self.write({
            'state': state,
        })


    @api.multi
    def set_active(self):        
        self.write({'state': 'Active', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
            self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.multi
    def set_inactive(self):
        self.write({'state': 'Inactive', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
            self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.multi
    def toggle_focus(self):
        for self in self:
            self.focus = '1' if self.focus == '0' else '0'
        if not self.env.context.get('group_by'):
            self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def _open_task_count(self):
        self.open_task_count = len(self.with_context(
            {'active_test': False}).env['nibbana.task'].search([
                ('project','=', self.id),
                ('state','not in',['Done','Cancelled'])
        ]))

    @api.one
    def _closed_task_count(self):
        self.closed_task_count = len(self.with_context(
            {'active_test': False}).env['nibbana.task'].search([
                ('project','=', self.id),
                ('state','in',['Done','Cancelled'])
        ]))


    @api.one
    def _reference_count(self):
        self.reference_count = len(self.with_context(
            {'active_test': False}).env['nibbana.reference'].search([
                ('project','=', self.id)]))



    @api.multi
    def _get_context(self):
        for self in self:
            self.context = [k.context_id.id for k in self.env[
                'nibbana.context_project'].search([
                    ('create_uid','=',self.env.user.id),
                    ('project_id','=', self.id)])]


    @api.multi
    def _set_context(self):
        for self in self:
            old = set(self.env['nibbana.context_project'].search([
                    ('create_uid','=',self.env.user.id),
                    ('project_id','=', self.id)]))
            new = set(self.context)
            to_add = new - old
            to_remove = old - new
            for c in to_add:
                self.env['nibbana.context_project'].create({
                    'project_id': self.id,
                    'context_id': c.id
                })
            for c in to_remove:
                c.unlink()


    def _search_context(self, operator, value):
        if operator == 'ilike':        
            context_ids = [k.id for k in self.env['nibbana.context'].search([
                ('create_uid','=',self.env.user.id),
                ('name', 'ilike', value)
            ])]
            project_context_ids = [k.project_id.id for k in self.env[
                                'nibbana.context_project'].search([
                        ('create_uid','=',self.env.user.id),
                        ('context_id', 'in', context_ids)])]
            return [('id', 'in', project_context_ids)]
        elif operator in ['in', '=']:
            if not type(value) is list:
                value = [value]
            project_context_ids = [k.project_id.id for k in self.env[
                                    'nibbana.context_project'].search([
                        ('create_uid','=',self.env.user.id),
                        ('context_id', 'in', value)])]            
            return [('id', 'in', project_context_ids)]
        else:
            raise ValidationError(_('Search context by {} not implemented!').format(operator))


    ######### AREA  #######
    #######################

    @api.multi
    def _get_area(self):
        for self in self:
            area = self.env['nibbana.area_project'].search([
                    ('create_uid','=',self.env.user.id),
                    ('project_id','=', self.id)], limit=1)
            self.area = area.area_id if area else False


    @api.multi
    def _set_area(self):
        for self in self:
            if not self.area:
                continue
            area = self.env['nibbana.area_project'].search([
                    ('create_uid','=',self.env.user.id),
                    ('project_id','=', self.id)])
            if not area:
                self.env['nibbana.area_project'].create({
                    'project_id': self.id,
                    'area_id': self.area.id
                })
            else:
                area.area_id = self.area.id


    def _search_area(self, operator, value):
        if operator == 'ilike':
            area = self.env['nibbana.area'].search([('name', 'ilike', value)])
            if not area:
                return [('id','=', False)]
            projects = self.env['nibbana.area_project'].search([
                ('create_uid','=', self.env.user.id),
                ('area_id','in',[k.id for k in area])])
            return [('id','in', [k.project_id.id for k in projects])]        
        elif operator in ['in', '=']:
            if not type(value) is list:
                value = [value]
            projects_area_ids = [k.project_id.id for k in self.env[
                                    'nibbana.area_project'].search([
                        ('create_uid','=',self.env.user.id),
                        ('area_id', 'in', value)])]            
            return [('id', 'in', projects_area_ids)]
        else:
            raise ValidationError(_('Search area by {} not implemented!').format(operator))



    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'context' in groupby:
            # Get the list of contexts
            res = []
            projects = self.env['nibbana.project'].search(domain)
            projects_ids = [k.id for k in projects]

            for c in self.env['nibbana.context'].search([
                                    ('create_uid','=', self.env.user.id)]):
                
                project_context_all = self.env['nibbana.context_project'].search([
                                        ('create_uid','=', self.env.user.id),
                                        ('context_id', '=', c.id)])
                project_context = project_context_all.filtered(
                                    lambda r: r.project_id.id in projects_ids)
                project_context_ids = [k.project_id.id for k in project_context]
                count = len(project_context_ids)

                if count:
                    res.append({
                        'context': (c.id, c.name),
                        'context_count': count,
                        '__domain': expression.AND([domain, 
                                        [('id','in', project_context_ids)]])
                    })
            return res

        elif 'area' in groupby:
            # Get the list of areas
            res = []
            projects = self.env['nibbana.project'].search(domain)
            projects_ids = [k.id for k in projects]
            for a in self.env['nibbana.area'].search([
                                    ('create_uid','=', self.env.user.id)]):
                project_areas_all = self.env['nibbana.area_project'].search([
                                        ('create_uid','=', self.env.user.id),
                                        ('area_id', '=', a.id)])
                project_areas = project_areas_all.filtered(
                                    lambda r: r.project_id.id in projects_ids)
                project_areas_ids = [k.project_id.id for k in project_areas]
                count = len(project_areas_ids)
                if count:
                    res.append({
                        'area': (a.id, a.name),
                        'area_count': count,
                        '__domain': expression.AND([domain, 
                                        [('id','in', project_areas_ids)]])
                    })
            # Find projects without area
            
            empty_projects = projects.filtered(
                lambda r: self.env['nibbana.area_project'].search_count([
                                    ('create_uid','=', self.env.user.id),
                                    ('project_id','=',r.id)]) == 0)
            empty_projects_ids = [k.id for k in empty_projects]

            if empty_projects_ids:
                res.append({
                    'area': (None, _('Undefined')),
                    'area_count': len(empty_projects),
                    '__domain': expression.AND([domain, 
                                        [('id','in', empty_projects_ids)]])
                })

            return res

        else:
            return  super(Project, self).read_group(domain, fields, groupby,
                offset, limit, orderby, lazy)


    @api.multi
    def _get_area_color(self):
        for self in self:
            self.area_color = self.area.color


    @api.depends('context')
    def _has_context(self):
        for self in self:
            if self.context:
                self.has_context = True
            else:
                self.has_context = False


    def _context_list(self):
        for self in self:
            self.context_list = ', '.join([k.name for k in self.context])


    def set_multi_state(self, state):
        self.browse(self.env.context.get('active_ids')).write({
            'state': state,
        })
        

    @api.model
    def move_scheduled_to_active(self):
        # Take all waiting tasks and escalate projects
        today = fields.Date.today()
        for project in self.search([('state','=','Scheduled'),
                                    ('schedule_start_date','<=', today)]):
            project.write({
                'state': 'Active',
            })

    @api.model
    def activate_user_projects(self):
        self.env['nibbana.project_inactive'].activate_user_projects()



class ProjectContext(models.Model):
    _name = 'nibbana.context_project'
    
    project_id = fields.Many2one('nibbana.project', required=True, ondelete='cascade')
    context_id = fields.Many2one('nibbana.context', required=True, ondelete='cascade')



class ProjectArea(models.Model):
    _name = 'nibbana.area_project'
    
    project_id = fields.Many2one('nibbana.project', required=True, ondelete='cascade')
    area_id = fields.Many2one('nibbana.area', required=True, ondelete='cascade')



class InactiveProject(models.Model):
    _name = 'nibbana.project_inactive'

    user = fields.Many2one('res.users', required=True, index=True, ondelete='cascade')
    project = fields.Many2one('nibbana.project', required=True, ondelete='cascade')


    @api.model
    def deactivate_projects(self):
        for s in self.env['nibbana.settings'].search(
                                    [('daily_refocus','=', True)]):
            user_projects = self.env['nibbana.project'].search([
                ('create_uid', '=', s.create_uid.id),
                ('state', '=', 'Active')
            ])
            if user_projects:
                self.env['nibbana.project_inactive'].search(
                                            [('user','=', s.create_uid.id)]).unlink()
                for p in user_projects:
                    self.env['nibbana.project_inactive'].create({
                        'user': s.create_uid.id,
                        'project': p.id
                    })
                    p.with_context({'tracking_disable': True}).write(
                                                        {'state': 'Inactive'})


    @api.model
    def activate_user_projects(self, user_id=None):
        if not user_id:
            user_id = self.env.user.id
        user_projects = self.env['nibbana.project_inactive'].search(
                                                    [('user','=', user_id)])
        for p in user_projects:
            try:
                if p.project.state == 'Inactive':
                    p.project.state = 'Active'
            except MissingError:
                # The project was deleted
                continue



class ProjectArea(models.TransientModel):
    _name = 'nibbana.project_area'

    new_area = fields.Many2one(comodel_name='nibbana.area', required=True)

    @api.one
    def do_change_area(self):
        projects = self.env['nibbana.project'].browse(self._context.get(
                                                        'active_ids', []))
        projects.write({'area': self.new_area.id})
        return {}
