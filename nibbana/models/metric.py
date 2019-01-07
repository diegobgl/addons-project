import logging
from odoo import models, fields, api, _

logger = logging.getLogger(__name__)


class Counter(models.Model):
    _name = 'nibbana.metric_counter'
    _log_access = False

    owner = fields.Many2one('res.users', required=True)
    code = fields.Char(required=True, index=True)
    name = fields.Char(required=True, index=True)
    value = fields.Integer(required=True)
    metric_date = fields.Date(default=fields.Date.today, index=True)

    _sql_constraints = [
        (
            'uniq_idx',
            'UNIQUE(owner,code,metric_date)',
            _('This metric is already created for this day and user!')
        )
    ]


    @api.model
    def scrap_counters(self):
        self.scrap_projects_states()
        self.scrap_tasks_states()


    def scrap_projects_states(self):
        states = ['Active', 'Inactive', 'Waiting', 'Scheduled', 'Done', 'Cancelled']
        for state in states:
            domain = [('state','=', state)]
            if state in ['Done', 'Cancelled']:
                domain.append(('write_date', '>', fields.Date.today()))
            projects = self.with_context(active_test=False).env[
                                            'nibbana.project'].search(domain)
            users = projects.mapped('create_uid')
            for user in users:
                user_projects = projects.filtered(
                                            lambda x: x.create_uid == user)
                # Search if we have a metric for this day
                metric = self.env['nibbana.metric_counter'].search([
                    ('owner','=',user.id), 
                    ('code','=', 'projects_state_{}'.format(state.lower())),
                    ('metric_date','=', fields.Date.today())
                ])
                if metric:
                    metric.value = len(user_projects)
                else:
                    metric = self.env['nibbana.metric_counter'].create({
                        'owner': user.id,
                        'name': state,
                        'code': 'projects_state_{}'.format(state.lower()),
                        'metric_date': fields.Date.today(),
                        'value': len(user_projects),
                    })



    def scrap_tasks_states(self):
        states = ['Next', 'Today', 'Tomorrow', 'Someday', 
                  'Waiting', 'Scheduled', 'Cancelled', 'Done']
        for state in states:
            domain = [('state','=', state)]
            if state in ['Done', 'Cancelled']:                
                domain.append(('write_date', '>', fields.Date.today()))            
            projects = self.with_context(active_test=False).env[
                                                'nibbana.task'].search(domain)
            users = projects.mapped('create_uid')
            for user in users:
                user_projects = projects.filtered(
                                            lambda x: x.create_uid == user)
                # Search if we have a metric for this day
                metric = self.env['nibbana.metric_counter'].search([
                    ('owner','=',user.id), 
                    ('code','=', 'tasks_state_{}'.format(state.lower())),
                    ('metric_date','=', fields.Date.today())
                ])
                if metric:
                    metric.value = len(user_projects)
                else:
                    metric = self.env['nibbana.metric_counter'].create({
                        'owner': user.id,
                        'name': state,
                        'code': 'tasks_state_{}'.format(state.lower()),
                        'metric_date': fields.Date.today(),
                        'value': len(user_projects),
                    })


