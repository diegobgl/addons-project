from odoo import models, fields


class User(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    nibbana_settings = fields.One2many('nibbana.settings',
                                       inverse_name='create_uid')
