import logging
from odoo import models, fields, api, _


logger = logging.getLogger(__name__)


class Settings(models.Model):
    _name = 'nibbana.settings'
    _description = 'Nibbana Settings'


    name = fields.Char(compute='_get_name')
    daily_refocus = fields.Boolean()

    _sql_constraints = [
        ('create_uid_uniq', 'unique (create_uid)', _('Settings record is already created!')),
    ]


    @api.multi
    def _get_name(self):
        for self in self:
            self.name = _('Nibbana Settings')


    def open_settings_form(self):
        s = self.env['nibbana.settings'].search([('create_uid','=', self.env.user.id)])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'nibbana.settings',
            'res_id': s.id if s else False,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }
