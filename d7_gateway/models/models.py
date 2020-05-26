# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests
import json


class D7smsTemplate(models.Model):
    _name = 'sms.template'

    name = fields.Char("Name")
    content = fields.Text("Content")


class D7Main(models.Model):
    _name = 'sms.model'
    _description = 'SMS Main Table for D7 sms Odoo Integration'
    _rec_name = 'message_id'

    to_address = fields.Char(string="To")
    employee_id = fields.Char(string="Employee")
    to = fields.Many2one("res.partner", string="Partner")
    to_list = fields.Many2many("res.partner", string="Partners")
    batch = fields.Boolean(default=False, string="Batch")
    template_id = fields.Many2one("sms.template", string="Template")
    content = fields.Text("Content")
    status = fields.Selection([('sent', 'Sent'), ('fail', 'Failed'), ('draft', 'Draft')], default='draft')
    message_id = fields.Char(string="Message Id")
    message_log = fields.Char(string="Message Log")

    @api.onchange('batch')
    def onchange_batch(self):
        """

        :return:
        """
        for record in self:
            if record.batch:
                record.to = False
            else:
                record.template_id = False

    @api.onchange('template_id')
    def onchange_template_id(self):
        """
        Onchange event to get the content defined in template
        :return:
        """
        for record in self:
            if record.template_id and record.template_id.content:
                record.content = record.template_id.content  # fetch template content and given to wizard

    def send_sms(self, action=False, test=False, to=False, content=False, batch=False, data=False):
        """
        basic sms function to send sms, which can be called from any model.
        data format:
            {'globals': {'from': 'Hilar'}, 'messages': [{'content': 'Dear Agrolait,\n\nyour invoice due should clear before 12/12/2018', 'to': ['+917736***']},
             {'content': 'Dear Edward Foster,\n\nyour invoice due should clear before 12/12/2018', 'to': ['+9177366*****']},]}
        :param test: boolean, true if it is testing from config
        :param to: mandatory, Destination address, only one address is supported per request
        :param content: Content to be sent
        :param batch: sms can be send for single address or as a batch
        :return: the response object
        """

        IrDefault = self.env['ir.default'].sudo()
        username = IrDefault.get('res.config.settings', 'username')
        password = IrDefault.get('res.config.settings', 'password')
        source = IrDefault.get('res.config.settings', 'source')
        batch = batch or self.batch
        url = 'http://rest-api.d7networks.com/secure/sendbatch' if batch else 'http://rest-api.d7networks.com/secure/send'
        sms_objects = False
        if test and to:
            data = {
                'to': to.strip().replace("+", ""),
                'content': "Test SMS",
                'from': "Admin"
            }
        elif not data:
            if not batch:
                data = {
                    'to': self.to.mobile or self.to.phone,
                    'content': content or self.content.format(name=self.to.name),
                    'from': source or '',
                }
            else:
                data = {
                    "globals": {
                        "from": source,
                    },
                    "messages": []
                }
                for person in self.to_list:  # to_list is a list of participants
                    if person.mobile or person.phone:
                        try:
                            data['messages'].append({
                                "to": [person.mobile and person.mobile.strip() or person.phone.strip()],
                                "content": self.content and self.content.format(name=person.name)
                            })
                        except Exception as e:
                            raise UserError(_("Template is not allowed to send SMS directly."))
                    else:
                        continue
        elif data:
            sms_objects = data.pop('sms_objects')
        else:
            pass
        # http://sms.d7networks.com:8080/secure/send
        r = requests.post(url,
                          auth=(username and username.strip(), password and password.strip()),
                          data=json.dumps(data))
        response = eval(r.text)
        if not self and sms_objects:
            sms_records = self.browse(sms_objects).sudo()
            # res = self.sudo().create()
            sms_records.write({
                'status': 'sent' if r.status_code == 200 else 'fail',
                'message_id': response.get('data')['batchId'] if batch else response.get('data'),
                'message_log': r.text,
            })
        if not batch:
            self.write({
                    'to_address': self.to.mobile or self.to.phone,})
        res = self
        if not test and res:
            if r.status_code == 200:
                res.status = 'sent'
                res.message_id = response.get('data')['batchId'] if batch else response.get('data')
            else:
                res.status = 'fail'
                res.message_id = ''
            res.message_log = r.text
        else:
            if r.status_code == 200:
                pass
        return r
