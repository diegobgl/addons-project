# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def sms_notify(self, create=False):
        """
        Function return the data to send.
        :return:
        """
        IrDefault = self.env['ir.default'].sudo()
        template_id = IrDefault.get('res.config.settings', 'project_sms_template') if not create else\
            IrDefault.get('res.config.settings', 'project_sms_template_create')
        if not template_id:
            raise ValidationError("Please Configure SMS Templates")
        if not self.partner_id:
            return False
        phone = self.partner_id.mobile or self.partner_id.phone
        if not (self.partner_id.mobile or self.partner_id.phone):
            # raise ValidationError("Please set Mobile or Work Phone for Customer")
            return
        template_id = self.env['sms.template'].sudo().browse(template_id)
        current_user = self.env.user.partner_id
        try:
            data = {
                'to': phone.strip(),
                'content': template_id.content and template_id.content.format(name=self.partner_id.name,
                                                                              task=self.name,
                                                                              project=self.project_id.name,
                                                                              stage=self.stage_id.name),
                'partner_id': self.partner_id.id or False,
                'template_id': template_id.id,
            }
        except Exception as e:
            raise ValidationError(_("Please Configure your SMS Template Correctly."))
        res = self.env['sms.model'].sudo().create({
            'to': data.pop('partner_id'),
            'to_address': data['to'],
            'template_id': data.pop('template_id'),
            'content': data.get('content'),
        })
        data["obj"] = res.id
        return data


    @api.model
    def create(self, vals):
        """
        Overrided to notify customer about new task creation
        :param vals:
        :return:
        """
        IrDefault = self.env['ir.default'].sudo()
        source = IrDefault.get('res.config.settings', 'source')
        data = {
            "globals": {
                "from": source,
            },
            "messages": [],
            "sms_objects": [],
        }
        task = super(ProjectTask, self).create(vals)
        result = task.sms_notify(create=True)
        if result:
            data["sms_objects"].append(result.pop('obj'))
            data["messages"].append(result)

        if data.get("messages", 0):
            self.env['sms.model'].sudo().send_sms(data=data, batch=True, )  # sending sms
        return task

    # CRUD Override
    @api.multi
    def write(self, vals):
        """
        overrided to notify customer about task's stage changes
        :param vals:
        :return:
        """
        IrDefault = self.env['ir.default'].sudo()
        source = IrDefault.get('res.config.settings', 'source')
        data = {
            "globals": {
                "from": source,
            },
            "messages": [],
            "sms_objects": [],
        }
        task = super(ProjectTask, self).write(vals)
        if 'stage_id' in vals:
            result = self.sms_notify()
            if result:
                data["sms_objects"].append(result.pop('obj'))
                data["messages"].append(result)
        if data.get("messages", 0):
            self.env['sms.model'].sudo().send_sms(data=data, batch=True, )  # sending sms
        return task

