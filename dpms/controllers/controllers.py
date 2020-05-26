# -*- coding: utf-8 -*-
from odoo import http
import xlsxwriter
import datetime
## Python 3
from io import BytesIO
import logging

class DpmsController(http.Controller):
    @http.route('/dpms/project/<int:id>/', auth='user')
    def project_export(self, **kwargs):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        values = dict(kwargs)
        id = values['id']
        project = http.request.env['dpms.project'].browse(id)
        bold = workbook.add_format({'bold': True})

        worksheet.write('A1','Project Title',bold)
        worksheet.write(0, 1, project.title )
        worksheet.write('A2', 'Reporting Date',bold)
        worksheet.write(1, 1, datetime.datetime.today().strftime('%Y-%m-%d'))
        worksheet.write('A3', 'Issues',bold)

        worksheet.write('B5', 'Title',bold)
        worksheet.write('C5', 'Impact', bold)
        worksheet.write('D5', 'Owner', bold)
        worksheet.write('E5', 'Resolution Date', bold)
        worksheet.write('F5', 'Status', bold)

        i=6
        for issue in project.issue_ids:
            worksheet.write(i,1,issue.title)
            worksheet.write(i,2,issue.impact)
            if issue.owner_id.name:
                worksheet.write(i, 3, issue.owner_id.name)
            worksheet.write(i, 4, issue.resolution_date)
            worksheet.write(i, 5, issue.status)
            i = i + 1
        i = i + 2
        worksheet.write('A'+ str(i), 'Ready by', bold)
        i = i + 1
        worksheet.write('A' + str(i), 'Duration', bold)
        worksheet.write('B' + str(i), project.duration)
        i = i + 1
        worksheet.write('A' + str(i), 'Start Date', bold)
        worksheet.write('B' + str(i), project.start_date)
        i = i + 1
        worksheet.write('A' + str(i), 'End Date', bold)
        worksheet.write('B' + str(i), project.end_date)
        workbook.close()
        output.seek(0)
        xlshttpheaders = [('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                          ('Content-Disposition', 'attachment; filename=project_report-'+project.title+'.xlsx')]
        return http.request.make_response(output.read(), xlshttpheaders)

    @http.route('/dpms/projectplanning/<int:id>/', auth='user')
    def project_planning_export(self, **kwargs):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        values = dict(kwargs)
        id = values['id']
        project = http.request.env['dpms.project'].browse(id)

        worksheet.write('A1','Project Title',bold)
        if project.title:
            worksheet.write('B1',project.title)

        worksheet.write('A2', 'Project Type', bold)
        if project.category:
            worksheet.write('B2', project.category)

        worksheet.write('A3', 'Project Priority', bold)
        if project.priority:
            worksheet.write('B3', project.priority)

        worksheet.write('A4', 'Description', bold)
        if project.description:
            worksheet.write('B4', project.description)

        worksheet.write('A5', 'Ready by', bold)
        if project.ready:
            worksheet.write('B5', project.ready)

        worksheet.write('A6', 'Budget & Resources', bold)
        if project.budget_resources:
            worksheet.write('B6', project.budget_resources)

        worksheet.write('B7','Project Management', bold)

        worksheet.write('A9', 'Project Manager', bold)
        if project.projectmanager_id.name:
            worksheet.write('B9', project.projectmanager_id.name)

        worksheet.write('A10', 'Owner Department', bold)
        if project.owner_id.name:
            worksheet.write('B10', project.owner_id.name)

        worksheet.write('A11', 'Stakeholders:', bold)
        i= 11
        for item in  project.stakeholder_ids:
            if item.department_id.name:
                worksheet.write(i,1, item.department_id.name)
            i = i + 1
        workbook.close()
        output.seek(0)
        xlshttpheaders = [('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                          ('Content-Disposition', 'attachment; filename=project_planning_report-'+project.title+'.xlsx')]
        return http.request.make_response(output.read(), xlshttpheaders)
