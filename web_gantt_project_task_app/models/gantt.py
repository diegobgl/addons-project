# -*- coding: utf-8 -*-

from odoo import fields, models, api, _ , tools
from openerp.exceptions import Warning
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import random
import base64
from datetime import datetime, timedelta,date
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class GanttView(models.Model):
	_inherit = 'project.project'

	def get_gantt_data(self):
		min_date_assign = []
		max_date_deadline = []
		all_projects = []
		all_dates = []

		project_ids = self.env['project.project'].search([])
		for project in project_ids:
			children = []
			all_dates = []
			for task in project.task_ids.filtered(lambda task: task.project_id == project):
				actualStart = ''
				actualEnd =''
				if task.date_assign:
					actualStart = task.date_assign
					all_dates.append(actualStart)

				if task.date_deadline:
					child_date_deadline  = datetime.strptime(task.date_deadline,  "%Y-%m-%d").date()
					final_date_deadline = child_date_deadline + timedelta(days=1)
					actualEnd = final_date_deadline.strftime("%Y-%m-%d")
					all_dates.append(actualEnd)
				if actualStart and actualEnd :
					children.append({
						'id': task.id,
						'name': task.name,
						'actualStart': actualStart,
						'actualEnd': actualEnd,
					})
			if children :
				all_projects.append({
					'id': project.id,
					'name': project.name,
					'actualStart': min(all_dates),
					'actualEnd'  : max(all_dates),
					'children': children
				})
		return all_projects