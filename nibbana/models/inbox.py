import logging
from odoo import fields, models, api, _


logger = logging.getLogger(__name__)


class Inbox(models.Model):
    _name = 'nibbana.inbox'
    _order = 'sequence, name'


    sequence = fields.Integer(default=1)
    name = fields.Char(required=True)
    note = fields.Html()
    area = fields.Many2one(comodel_name='nibbana.area', ondelete='cascade')
    area_color = fields.Char(related='area.color')
    context = fields.Many2many(comodel_name='nibbana.context', ondelete='cascade')
    context_list = fields.Char(compute='_context_list', string=_('Context'))


    @api.depends('context')
    def _context_list(self):
        for self in self:
            self.context_list = ', '.join([k.name for k in self.context])

    @api.multi
    def convert_to_project(self):
        self.ensure_one()
        project = self.env['nibbana.project'].create({
            'name': self.name,
            'note': self.note,                
            'area': self.area.id,
            'context': [k.id for k in self.context] if self.context else False,
        })
        self.unlink()
        return {     
             'type': 'ir.actions.act_window',
             'name': 'Project',   
             'res_model': 'nibbana.project',   
             'view_type': 'form',    
             'view_mode': 'form,tree', # If here is tree,form res_id will not work!
             'target': '',
             'res_id': project.id
        }


    @api.multi
    def convert_to_task(self):
        self.ensure_one()
        task = self.env['nibbana.task'].create({
            'name': self.name,
            'note': self.note,                
            'area': self.area.id,
            'context': [k.id for k in self.context] if self.context else False,
        })
        self.unlink()
        return {     
             'type': 'ir.actions.act_window',
             'name': 'Task',   
             'res_model': 'nibbana.task',   
             'view_type': 'form',    
             'view_mode': 'form,tree', # If here is tree,form res_id will not work!
             'target': '',
             'res_id': task.id
        }


    @api.multi
    def convert_to_reference(self):
        self.ensure_one()
        ref = self.env['nibbana.reference'].create({
            'name': self.name,
            'content': self.note,                
            'reference_area': self.area.id,
        })
        self.unlink()
        return {     
             'type': 'ir.actions.act_window',
             'name': 'Reference',   
             'res_model': 'nibbana.reference',
             'view_type': 'form',    
             'view_mode': 'form,tree', # If here is tree,form res_id will not work!
             'target': '',
             'res_id': ref.id
        }


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):        
        default = dict(default or {})
        default.update({'uid': generate_uid(self)})
        return super(Inbox, self).copy(default)

