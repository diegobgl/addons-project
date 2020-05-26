# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning, except_orm


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    username = fields.Char("Username")
    password = fields.Char("Password")
    source = fields.Char("From")
    test_to = fields.Char("Testing Address")
    #
    module_d7_sms_hr = fields.Boolean("Notify employee leave approvals")
    module_d7_sms_hr_payroll = fields.Boolean("Notify Payroll Confirmation")
    hr_template_id = fields.Many2one('sms.template')  # for leave req
    hr_template_allocation = fields.Many2one('sms.template')  # for leave alloc
    hr_template_payroll = fields.Many2one('sms.template')
    #
    module_d7_sms_sales = fields.Boolean("Notify sale order confirmation")
    sale_sms_template = fields.Many2one('sms.template')
    #
    module_d7_sms_purchase = fields.Boolean("Notify purchase order confirmation")
    purchase_sms_template = fields.Many2one('sms.template')
    #
    module_d7_sms_project_tasks = fields.Boolean("Notify customer about project")
    project_sms_template = fields.Many2one('sms.template')
    project_sms_template_create = fields.Many2one('sms.template')
    #
    sms_hr_leave_flag = fields.Boolean(compute="get_modules_availability")
    sms_hr_payroll_flag = fields.Boolean(compute="get_modules_availability")
    sms_sales_flag = fields.Boolean(compute="get_modules_availability")
    sms_purchase_flags = fields.Boolean(compute="get_modules_availability")
    sms_project = fields.Boolean(compute="get_modules_availability")
    #

    @api.depends('sms_hr_leave_flag', 'sms_hr_payroll_flag', 'sms_sales_flag', 'sms_purchase_flags', 'sms_project')
    def get_modules_availability(self):
        """

        :return:
        """
        IrModule = self.env['ir.module.module'].sudo()
        sms_leave_flag = IrModule.search([('name', '=', 'd7_sms_hr')])
        sms_payroll_flag = IrModule.search([('name', '=', 'd7_sms_hr_payroll')])
        sms_project_flag = IrModule.search([('name', '=', 'd7_sms_project_tasks')])
        sms_purchase_flag = IrModule.search([('name', '=', 'd7_sms_purchase')])
        sms_sales_flag = IrModule.search([('name', '=', 'd7_sms_sales')])
        for record in self:
            if len(sms_leave_flag):
                record.sms_hr_leave_flag = True
            else:
                record.sms_hr_leave_flag = False
            if len(sms_payroll_flag):
                record.sms_hr_payroll_flag = True
            else:
                record.sms_hr_payroll_flag = False
            if len(sms_project_flag):
                record.sms_project = True
            else:
                record.sms_project = False
            if len(sms_purchase_flag):
                record.sms_purchase_flags = True
            else:
                record.sms_purchase_flags = False
            if len(sms_sales_flag):
                record.sms_sales_flag = True
            else:
                record.sms_sales_flag = False


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        # ONLY FOR v11. DO NOT FORWARD-PORT
        IrDefault = self.env['ir.default'].sudo()
        username = IrDefault.get('res.config.settings', 'username')
        password = IrDefault.get('res.config.settings', 'password')
        source = IrDefault.get('res.config.settings', 'source')
        test_to = IrDefault.get('res.config.settings', 'test_to')
        #
        hr_template_id = IrDefault.get('res.config.settings', 'hr_template_id')
        hr_template_allocation = IrDefault.get('res.config.settings', 'hr_template_allocation')
        hr_template_payroll = IrDefault.get('res.config.settings', 'hr_template_payroll')
        #
        sale_sms_template = IrDefault.get('res.config.settings', 'sale_sms_template')
        #
        purchase_sms_template = IrDefault.get('res.config.settings', 'purchase_sms_template')
        #
        project_sms_template = IrDefault.get('res.config.settings', 'project_sms_template')
        project_sms_template_create = IrDefault.get('res.config.settings', 'project_sms_template_create')

        res.update(
            username=username if username else False,
            password=password if password else False,
            test_to=test_to if test_to else False,
            source=source if source else False,
            hr_template_id=hr_template_id if hr_template_id else False,
            hr_template_allocation=hr_template_allocation if hr_template_allocation else False,
            hr_template_payroll=hr_template_payroll if hr_template_payroll else False,
            sale_sms_template=sale_sms_template if sale_sms_template else False,
            purchase_sms_template=purchase_sms_template if purchase_sms_template else False,
            project_sms_template=project_sms_template if project_sms_template else False,
            project_sms_template_create=project_sms_template_create if project_sms_template_create else False,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # ONLY FOR v11. DO NOT FORWARD-PORT
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings', 'username', self.username)
        IrDefault.set('res.config.settings', 'password', self.password)
        IrDefault.set('res.config.settings', 'test_to', self.test_to)
        IrDefault.set('res.config.settings', 'source', self.source)
        IrDefault.set('res.config.settings', 'hr_template_id', self.hr_template_id.id)
        IrDefault.set('res.config.settings', 'hr_template_allocation', self.hr_template_allocation.id)
        IrDefault.set('res.config.settings', 'hr_template_payroll', self.hr_template_payroll.id)
        IrDefault.set('res.config.settings', 'sale_sms_template', self.sale_sms_template.id)
        IrDefault.set('res.config.settings', 'purchase_sms_template', self.purchase_sms_template.id)
        IrDefault.set('res.config.settings', 'project_sms_template', self.project_sms_template.id)
        IrDefault.set('res.config.settings', 'project_sms_template_create', self.project_sms_template_create.id)

    @api.multi
    def test_sms(self):
        """
        Function invokes when using test button under config
        :return:
        """
        self.ensure_one()
        sms = self.env['sms.model'].sudo()
        result = sms.send_sms(test=True, to=self.test_to)
        raise Warning(result.text)