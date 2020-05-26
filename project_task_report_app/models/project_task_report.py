# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountAnalyticLine(models.Model):
	_inherit = 'account.analytic.line'

	acc_analytic_line_id = fields.Many2one('account.analytic.line')

class TaskDetails(models.TransientModel):
	_name = 'task.details'

	user_id = fields.Many2one('res.users', string='User', required=True)
	start_date = fields.Datetime(string='Start Date', required=True)
	end_date = fields.Datetime(string='End Date', required=True)

	acc_analytic_line_ids = fields.One2many('account.analytic.line','acc_analytic_line_id')

	@api.onchange('user_id','start_date','end_date')
	def onchange_order(self):
		if self.user_id:
			task_id =  self._context.get('active_id')
			get_rec_lines  = self.env['account.analytic.line'].search([('user_id','=',self.user_id.id),('task_id','=',task_id), ('task_id.date_deadline','>', self.start_date),('task_id.date_deadline','<',self.end_date)])
			list_line = []
			for line in get_rec_lines:
				list_line.append(line.id)
			self.update({'acc_analytic_line_ids':[(6,0,list_line)]})

	@api.multi
	def print_task_report(self):
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'task_id':self.env.context.get('active_id'),
				'user_id': self.user_id.id,
				'start_date': self.start_date,
				'end_date':self.end_date,
			},
		}
		return self.env.ref('project_task_report_app.task_report_template').report_action(self, data=data)

class TaskReport(models.AbstractModel):
	_name = 'report.project_task_report_app.task_template_report'
	_description = "Project Task Report"

	@api.model
	def get_report_values(self, docids, data=None):
		user_id = data['form']['user_id']
		start_date = data['form']['start_date'] 
		end_date = data['form']['end_date']
		get_task_id = data['form']['task_id']
		docs = []
		task_id = self.env['project.task'].browse(get_task_id)
		timesheet_ids = self.env['account.analytic.line'].search([('user_id','=',user_id),('task_id','=',task_id.id), ('task_id.date_deadline','>',str(start_date)),('task_id.date_deadline','<',str(end_date))])
		for task in timesheet_ids:
			docs.append({
				'date': task.date,
				'employee_id': task.employee_id.name,
				'name':task.name,
				'unit_amount': task.unit_amount,
			})
		
		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'docs': docs,
			'task_id':task_id,
			'start_date':start_date,
			'end_date':end_date,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: