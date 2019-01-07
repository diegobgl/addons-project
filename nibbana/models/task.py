from datetime import datetime, date
from dateutil.relativedelta import  relativedelta
import logging
from .utils import generate_uid
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from .utils import increment_metric, decrement_metric

logger = logging.getLogger(__name__)


_intervalTypes = {
    'day': lambda interval: relativedelta(days=interval),
    'week': lambda interval: relativedelta(days=7*interval),
    'month': lambda interval: relativedelta(months=interval),
    'year': lambda interval: relativedelta(months=12*interval),
}

STATES = (        
        ('Today', _('Today')),
        ('Tomorrow', _('Tomorrow')),
        ('Next', _('Next')),
        ('Waiting', _('Waiting')),
        ('Scheduled', _('Scheduled')),
        ('Someday', _('Someday')),
        ('Done', _('Done')),
        ('Cancelled', _('Cancelled')),
    )



class Task(models.Model):
    _name = 'nibbana.task'
    _description = _('Task')
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True)
    note = fields.Html()
    project = fields.Many2one('nibbana.project', ondelete='cascade')
    area_color = fields.Char(compute=lambda self: self._get_area_color())
    area = fields.Many2one(comodel_name='nibbana.area',
                               compute='_get_area', inverse='_set_area',
                               search='_search_area')   
    project_state = fields.Selection(related='project.state', store=True,
                                     string='Project state')
    context = fields.Many2many(comodel_name='nibbana.context',
                               compute='_get_context', inverse='_set_context',
                               search='_search_context')    
    context_list = fields.Char(compute='_context_list', string=_('Context'))
    schedule_start_date = fields.Date()
    interval_type = fields.Selection(selection=[('day', _('Every Day')),
                                                ('week', _('Every Week')),
                                                ('month', _('Every Month')),
                                                ('year', _('Every Year'))],
                                     string=_('Interval'))
    wait_till = fields.Date(string=_('Wait untill'))
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=STATES, default='Next', 
                             index=True, required=True)
    state_changed = fields.Datetime(default=fields.Datetime.now, string=_('Changed'))
    state_change_count = fields.Integer(default=0, string=_('Changes'))
    focus = fields.Selection(selection=(
        ('0', _('Non-focused')),
        ('1', _('Focused'))), default='0')
    repeat = fields.Boolean()
    uid = fields.Char(required=True, index=True, size=32,
                      default=generate_uid)
    contacts = fields.Many2many('res.partner')


    _sql_constraints = [
        ('uid_uniq', 'UNIQUE(uid)', _('The uid must be unique !')),
    ]


    @api.model
    def create(self, vals):
        # Check focus
        if vals.get('state') and vals.get('state') == 'Today':
                vals['focus'] = '1'        
        res = super(Task, self).create(vals)
        increment_metric(self, name = _('Tasks'), code = 'tasks_created')
        self.env['nibbana.timeline'].timeline_create_event(res)
        return res


    @api.multi
    def unlink(self):
        for rec in self:
            self.env['nibbana.timeline'].timeline_unlink_event(rec)
        return super(Task, self).unlink()


    @api.multi
    def write(self, vals):                
        for rec in self:
            # Check focus remove attempt
            if not vals.get('state') and rec.state == 'Today' and vals.get('focus') == '0':
                raise ValidationError(_("You should keep focus on Today's tasks!")) 
            elif vals.get('state') == 'Today' and vals.get('focus') != '0':
                vals['focus'] = '1'
            # Check state change
            if vals.get('state') and vals.get('state') != 'Today':
                vals['focus'] = '0'
            if not vals.get('state_change_count') and ('state' in vals or 'focus' in vals):
                vals['state_change_count'] = rec.state_change_count + 1
                vals['state_changed'] = datetime.now()
            if vals.get('state') and vals['state'] != 'Scheduled':
                vals['schedule_start_date'] = False
                vals['repeat'] = False
            if vals.get('state'):
                increment_metric(rec, code='tasks_changed', name=_('Tasks'))
                if vals['state'] == 'Done' and rec.state != 'Done':
                    increment_metric(rec, code='tasks_done', name=_('Tasks'))
                elif vals['state'] != 'Done' and rec.state == 'Done':
                    decrement_metric(rec, code='tasks_done', name=_('Tasks'))
                # Archive
                if vals['state'] in ['Done', 'Cancelled']:
                    vals['active'] = False
                elif vals['state'] not in  ['Done', 'Cancelled']:
                    vals['active'] = True
            self.env['nibbana.timeline'].timeline_update_event(rec, vals,
                            ['state', 'name', 'project', 'focus'])
        super(Task, self).write(vals)
        return True


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):        
        default = dict(default or {})
        default.update({'uid': generate_uid(self)})
        return super(Task, self).copy(default)


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
                    if result['state'] in ['Done', 'Cancelled',
                                           'Scheduled', 'Someday']:
                        result['__fold'] = True
                return results

            else:
                return super(Task, self)._read_group_fill_results(
            domain, groupby, remaining_groupbys, aggregated_fields,
            count_field, read_group_result, read_group_order)


    @api.onchange('project')
    def set_context_by_project_context(self):
        if self.project:
            self.context = self.project.context
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



    @api.one
    def set_today(self):
        self.write({'state': 'Today', 'focus': '1', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def set_tomorrow(self):
        self.write({'state': 'Tomorrow', 'focus': '0', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def set_next(self):
        self.write({'state': 'Next', 'focus': '0', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def set_scheduled(self):
        self.write({'state': 'Scheduled','focus': '0'})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def set_done(self):
        self.write({'active': False, 'state': 'Done', 'focus': '0', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')    


    @api.one
    def set_waiting(self):
        self.write({'state': 'Waiting', 'focus': '0', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def set_someday(self):
        self.write({'state': 'Someday', 'focus': '0', 'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def set_cancelled(self):
        self.write({'active': False, 'state': 'Cancelled', 'focus': '0', 
                    'schedule_start_date': False})
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.one
    def invert_focus(self):
        self.focus = '1' if self.focus == '0' else '0'
        if not self.env.context.get('group_by'):
             self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.model
    def move_tasks_to_today(self):
        # Called from cron
        self.move_tomorrow_to_today()
        self.move_waiting_to_today()
        self.move_scheduled_to_today()


    def move_tomorrow_to_today(self):
        today = datetime.now().date()
        tasks = self.search([('state','=','Tomorrow')])
        tasks = tasks.filtered(
                lambda x: fields.Datetime.from_string(x.state_changed).date() < today)
        for task in tasks:
            # Omit completed projects
            if task.project and task.project.state in ['Done', 'Cancelled']:
                continue
            task.state = 'Today'
            if task.project:
                task.project.state = 'Active'
                

    def move_waiting_to_today(self):
        tasks = self.search([
            ('state','=','Waiting'),
            ('wait_till', '<=', fields.Date.today()),
        ])
        for task in tasks:
            # Omit completed projects
            if task.project and task.project.state in ['Done', 'Cancelled']:
                continue
            task.write({'state': 'Today', 'wait_till': False})
            if task.project:
                task.project.state = 'Active'


    def move_scheduled_to_today(self):
        # Take all waiting tasks and escalate projects
        today = fields.Date.today()
        for task in self.search([('state','=','Scheduled'),
                                 ('schedule_start_date','<=', today)]):
            # Omit completed projects
            if task.project and task.project.state in ['Done', 'Cancelled']:
                continue

            task.write({'state': 'Today', 'schedule_start_date': False})
            if task.project:
                task.project.state = 'Active'
            # Check repeatable
            if task.repeat:
                new_task = task.copy(default={
                    'state': 'Scheduled',
                    'schedule_start_date': datetime.strptime(
                                    today, '%Y-%m-%d') + \
                                    _intervalTypes[task.interval_type](1)})


    @api.constrains('wait_till')
    def _check_wait_till(self):
        if self.wait_till and self.wait_till <= fields.Date.today():
            raise ValidationError(_('You should set a future date!'))


    @api.constrains('focus')
    def _check_focus(self):
        if self.state == 'Today' and self.focus == '0':
            raise ValidationError(_("You should keep focus on Today's tasks!"))


    @api.constrains('schedule_start_date')
    def _check_schedule_start_date(self):
        if self.schedule_start_date and self.schedule_start_date <= fields.Date.today():
            raise ValidationError(_('You should set a future date!'))


    @api.multi # Critical for returning a view!
    def open_project_form(self):
        res = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'nibbana.project',
            'res_id': self.project[0].id,
            'target': 'current',
            'context': self._context.copy(),
        }
        return res


    @api.multi
    def convert_to_project(self):        
        tasks = self.browse(self.env.context.get('active_ids'))
        last_project_id = False
        for t in tasks:            
            p = self.env['nibbana.project'].create({
                'name': t.name,
                'note': t.note,
                'area': t.area.id,
                'state': 'Active',
                'focus': t.focus,
                'context': [k.id for k in t.context] if t.context else False,
            })
            last_project_id = p.id
            t.unlink()
        return {
            'name': 'Project',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'nibbana.project',
            'res_id': last_project_id,
            'target': 'current',
            'context': self._context.copy(),
        }



    def _context_list(self):
        for self in self:
            self.context_list = ', '.join([k.name for k in self.context])


    @api.multi
    def _get_context(self):
        for self in self:
            self.context = [k.context_id.id for k in self.env[
                'nibbana.context_task'].search([
                    ('create_uid','=',self.env.user.id),
                    ('task_id','=', self.id)])]


    @api.multi
    def _set_context(self):
        for self in self:
            old = set(self.env['nibbana.context_task'].search([
                    ('create_uid','=',self.env.user.id),
                    ('task_id','=', self.id)]))
            new = set(self.context)
            to_add = new - old
            to_remove = old - new
            for c in to_add:
                self.env['nibbana.context_task'].create({
                    'task_id': self.id,
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
            task_context_ids = [k.task_id.id for k in self.env[
                                    'nibbana.context_task'].search([
                        ('create_uid','=',self.env.user.id),
                        ('context_id', 'in', context_ids)])]
            return [('id', 'in', task_context_ids)]
        elif operator in ['in', '=']:
            if not type(value) is list:
                value = [value]
            task_context_ids = [k.task_id.id for k in self.env[
                                    'nibbana.context_task'].search([
                        ('create_uid','=',self.env.user.id),
                        ('context_id', 'in', value)])]            
            return [('id', 'in', task_context_ids)]
        else:
            raise ValidationError(_('Search context by {} not implemented!').format(operator))



    @api.multi
    def _get_area(self):
        for self in self:
            if not self.project:
                area = self.env['nibbana.area_task'].search([
                        ('create_uid','=',self.env.user.id),
                        ('task_id','=', self.id)], limit=1)
                self.area = area.area_id if area else False
            else:
                self.area = self.project.area


    @api.multi
    def _set_area(self):
        for self in self:
            if not self.area:
                continue
            area = self.env['nibbana.area_task'].search([
                    ('create_uid','=',self.env.user.id),
                    ('task_id','=', self.id)])
            if not area:
                self.env['nibbana.area_task'].create({
                    'task_id': self.id,
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
            tasks = self.env['nibbana.area_task'].search([
                ('create_uid','=', self.env.user.id),
                ('area_id','in',[k.id for k in area])])
            return [('id','in', [k.task_id.id for k in tasks])]
        
        elif operator in ['in', '=']:
            if not type(value) is list:
                value = [value]
            tasks_area_ids = [k.task_id.id for k in self.env[
                                    'nibbana.area_task'].search([
                        ('create_uid','=',self.env.user.id),
                        ('area_id', 'in', value)])]            
            return [('id', 'in', tasks_area_ids)]
        else:
            raise ValidationError(_('Search area by {} not implemented!').format(operator))



    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'context' in groupby:
            # Get the list of contexts
            res = []
            tasks = self.env['nibbana.task'].search(domain)
            tasks_ids = [k.id for k in tasks]

            for c in self.env['nibbana.context'].search([
                                    ('create_uid','=', self.env.user.id)]):
                
                task_context_all = self.env['nibbana.context_task'].search([
                                        ('create_uid','=', self.env.user.id),
                                        ('context_id', '=', c.id)])
                task_context = task_context_all.filtered(
                                    lambda r: r.task_id.id in tasks_ids)
                task_context_ids = [k.task_id.id for k in task_context]
                count = len(task_context_ids)

                if count:
                    res.append({
                        'context': (c.id, c.name),
                        'context_count': count,
                        '__domain': expression.AND([domain, 
                                        [('id','in', task_context_ids)]])
                    })
            return res

        elif 'area' in groupby:
            # Get the list of areas
            res = []
            areas = self.env['nibbana.area'].search([
                                    ('create_uid','=', self.env.user.id)],
                                    order='name')
            area_ids = dict([(a.id, []) for a in areas])
            area_ids[0] = []
            area_names = dict([(a.id, a.name) for a in areas])
            area_names[0] = _('Undefined')
            records = self.env[self._name].search(domain)
            for rec in records:
                if rec.project and rec.project.area:
                        area_ids[rec.project.area.id].append(rec.id)
                elif rec.area:
                        area_ids[rec.area.id].append(rec.id)
                else:
                    area_ids[0].append(rec.id)
            # Form result
            for area_id, id_list in area_ids.items():
                if len(id_list) == 0:
                    continue
                res.append({
                        'area': (area_id, area_names[area_id]),
                        'area_count': len(id_list),
                        '__domain': expression.AND([domain, 
                                        [('id','in', id_list)]])

                })
            return res
                     
        else:
            return  super(Task, self).read_group(domain, fields, groupby, 
                            offset, limit, orderby, lazy)


    @api.multi
    def _get_area_color(self):
        for self in self:
            self.area_color = self.area.color


class TaskContext(models.Model):
    _name = 'nibbana.context_task'
    
    task_id = fields.Many2one('nibbana.task', required=True, ondelete='cascade')
    context_id = fields.Many2one('nibbana.context', required=True, ondelete='cascade')


class TaskArea(models.Model):
    _name = 'nibbana.area_task'
    
    task_id = fields.Many2one('nibbana.task', required=True, ondelete='cascade')
    area_id = fields.Many2one('nibbana.area', required=True, ondelete='cascade')


class ScheduleTask(models.TransientModel):
    _name = 'nibbana.schedule_task'

    def _default_task(self):
        return self.env['nibbana.task'].browse(self._context.get('active_id'))

    def _default_start_date(self):
        return self._default_task().schedule_start_date

    task = fields.Many2one(comodel_name='nibbana.task', default=_default_task)
    new_start_date = fields.Date(required=True, default=_default_start_date)


    @api.one
    def do_schedule(self):
        self.task.write({
            'schedule_start_date': self.new_start_date,
            'state': 'Scheduled',
            'focus': '0',
            'state_changed': fields.Datetime.now(),
            'state_change_count': self.task.state_change_count + 1,
        })
        return {}



class WaitingTask(models.TransientModel):
    _name = 'nibbana.waiting_task'

    def _default_task(self):
        return self.env['nibbana.task'].browse(self._context.get('active_id'))

    def _default_wait_till(self):
        return self._default_task().wait_till

    task = fields.Many2one(comodel_name='nibbana.task', default=_default_task)
    new_wait_till = fields.Date(required=False, default=_default_wait_till)


    @api.one
    def do_waiting(self):
        self.task.write({
            'wait_till': self.new_wait_till,
            'state': 'Waiting',
            'focus': '0',
            'state_changed': fields.Datetime.now(),
            'state_change_count': self.task.state_change_count + 1,

        })
        return {}

