import logging
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

logger = logging.getLogger(__name__)


class Act(models.Model):
    _name = 'nibbana.act_view'
    _auto = False
    _sql = """
    DROP VIEW IF EXISTS nibbana_act_view CASCADE;
    CREATE VIEW nibbana_act_view AS
        SELECT row_number() OVER () AS id,
        np.id AS project_id,
        np.state AS project_state, 
        nt.id AS task_id,
        nt.state AS task_state,  nt.project AS task_project,
        CASE WHEN nt.id IS NOT NULL THEN 'task' ELSE 'project' END AS open_type,
        CASE 
            WHEN  nt.id IS NOT NULL AND np.id IS NOT NULL THEN nt.name || ' @ ' || np.name 
            WHEN  nt.id IS NOT NULL AND np.id IS NULL THEN nt.name
            ELSE np.name END AS name,
        CASE WHEN nt.id IS NOT NULL THEN nt.create_uid ELSE np.create_uid END AS user_id,
        CASE WHEN nt.id IS NOT NULL THEN nt.sequence ELSE np.sequence END AS sequence,
        CASE WHEN nt.id IS NOT NULL THEN nt.focus ELSE np.focus END AS focus,
        CASE WHEN nt.id IS NOT NULL THEN nt.state ELSE '' END AS state
        FROM nibbana_project AS np
            FULL OUTER JOIN nibbana_task AS nt ON (np.id=nt.project AND nt.state IN ('Next','Today'))
            WHERE (
                (np.id IS NOT NULL AND np.active = TRUE AND np.state = 'Active' 
                    AND nt.id IS NULL)
                OR 
                (np.id IS NOT NULL AND np.active = TRUE AND np.state = 'Active' 
                        AND nt.active = TRUE AND nt.state IN ('Next','Today')) 
                OR 
                  (np.id IS NULL AND nt.id IS NOT NULL AND nt.active = TRUE 
                        AND nt.state IN ('Next','Today')))
            ORDER BY sequence;
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    open_type = fields.Char()
    project_id = fields.Many2one('nibbana.project')
    task_id = fields.Many2one('nibbana.task')
    user_id = fields.Many2one('res.users')
    name = fields.Char()
    state = fields.Char()    
    focus = fields.Char()
    area = fields.Many2one(comodel_name='nibbana.area', compute='_get_area',
                           search='_search_area')
    area_color = fields.Char(compute=lambda self: self._get_area_color())
    context = fields.Many2many(comodel_name='nibbana.context',
                               compute='_get_context',
                               search='_search_context')    
    context_list = fields.Char(string=_('Context'), compute='_get_context_list')
    task_project = fields.Many2one('nibbana.project', string=_('Task Project'))   


    @api.multi
    def _get_context_list(self):
        for self in self:
            self.context_list = self.task_id.context_list if self.task_id else \
                self.project_id.context_list


    @api.multi
    def _get_area(self):
        for self in self:
            self.area = self.task_id.area if self.task_id else self.project_id.area


    @api.multi
    def _get_context(self):
        for self in self:
            self.context = self.task_id.context if self.task_id else self.project_id.context


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
            task_context_ids = [k.task_id.id for k in self.env[
                                    'nibbana.context_task'].search([
                        ('create_uid','=',self.env.user.id),
                        ('context_id', 'in', context_ids)])]
            return ['|', 
                        '&', '&', ('project_id','!=',False),
                                  ('task_id','=',False),
                                  ('project_id','in', project_context_ids),
                        ('task_id','in', task_context_ids)]
        else:
            raise ValidationError(_('Search context by {} not implemented!').format(operator))


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
            projects = self.env['nibbana.area_project'].search([
                ('create_uid','=', self.env.user.id),
                ('area_id','in',[k.id for k in area])])

            return ['|', 
                    '&', ('project_id','!=',False), 
                         ('project_id','in', [k.project_id.id for k in projects]),
                    '&', ('project_id','=',False), 
                         ('task_id','in', [k.task_id.id for k in tasks])
            ]
        else:
            raise ValidationError(_('Search area by {} not implemented!').format(operator))



    @api.multi
    def _get_area_color(self):
        for self in self:
            self.area_color = self.area.color


    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'area' in groupby:
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
                if rec.project_id and rec.project_id.area:
                        area_ids[rec.project_id.area.id].append(rec.id)
                elif rec.task_id and rec.task_id.area:
                        area_ids[rec.task_id.area.id].append(rec.id)
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
        elif 'context' in groupby:
            res = []
            contexts = self.env['nibbana.context'].search([
                                    ('create_uid','=', self.env.user.id)],
                                    order='name')
            context_ids = dict([(c.id, []) for c in contexts])
            context_ids[0] = []
            context_names = dict([(c.id, c.name) for c in contexts])
            context_names[0] = _('Undefined')
            records = self.env[self._name].search(domain)
            for rec in records:
                if rec.project_id and not rec.task_id and rec.project_id.context:
                    for c in rec.project_id.context:
                        context_ids[c.id].append(rec.id)
                elif rec.task_id and rec.task_id.context:
                    for c in rec.task_id.context:
                        context_ids[c.id].append(rec.id)
                else:
                    context_ids[0].append(rec.id)
            # Form result
            for context_id, id_list in context_ids.items():
                if len(id_list) == 0:
                    continue
                res.append({
                        'context': (context_id, context_names[context_id]),
                        'context_count': len(id_list),
                        '__domain': expression.AND([domain, 
                                        [('id','in', id_list)]])
                })                
            return res
        else:
            return super(Act, self).read_group(domain, fields, groupby,
                offset, limit, orderby, lazy)



    def open(self):
        self.ensure_one()
        res = {
            'type': 'ir.actions.act_window',
            'name': self.open_type.capitalize(),   
            'res_model': 'nibbana.{}'.format(self.open_type),
            'view_type': 'form',    
            'view_mode': 'form,tree', # If here is tree,form res_id will not work!
            'target': '',
            'res_id': self.project_id.id if self.open_type == 'project' \
                         else self.task_id.id
        }
        return res

    @api.multi
    def set_inactive(self):
        self.ensure_one()
        self.project_id.set_inactive()
        if not self.env.context.get('group_by'):
            self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.multi
    def set_done(self):
        self.ensure_one()
        self.task_id.set_done()
        if not self.env.context.get('group_by'):
            self.env['bus.bus'].sendone('tree_reload', 'reload')



    @api.multi
    def invert_focus(self):
        self.ensure_one()
        if self.open_type == 'task':
            self.task_id.invert_focus()
        else:
            self.project_id.toggle_focus()
        if not self.env.context.get('group_by'):
            self.env['bus.bus'].sendone('tree_reload', 'reload')


    @api.constrains('focus')
    def _check_focus(self):
        if self.state == 'Today' and self.focus == '0':
            raise ValidationError(_("You should keep focus on Today's tasks!"))
        

    @api.multi # Critical for returning a view!
    def open_project_form(self):
        res = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'nibbana.project',
            'res_id': self.project_id[0].id,
            'target': 'current',
            'context': self._context.copy(),
        }
        return res


class ActDistinct(Act):
    _name = 'nibbana.act_view_distinct'
    _sql = """
    DROP VIEW IF EXISTS nibbana_act_view_distinct;
    CREATE VIEW nibbana_act_view_distinct AS 
        SELECT DISTINCT ON (project_id) *  FROM 
        (
        SELECT id, CAST(COALESCE(project_id, RANDOM()*1000000000) AS INT) AS project_id, 
                task_id, task_project, open_type, 
                name, user_id, sequence, focus, state
        FROM nibbana_act_view
        )  p ORDER BY project_id, focus desc, sequence, name;

    """


