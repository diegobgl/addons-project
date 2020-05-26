 # -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Akshay Babu(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo.http import request
from odoo import models, api


class ProjectReportXls(models.AbstractModel):
    _name = 'report.project_report_pdf.project_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print('kskskjajaajaj')
        name = data['record']
        print(lines)
        print(data['context']['uid'])
        user_obj = self.env['res.users'].search([('id', '=', data['context']['uid'])])
        print(user_obj.company_id)
        wizard_record = request.env['wizard.project.report'].search([])[-1]
        task_obj = request.env['project.task']
        users_selected = []
        stages_selected = []
        for elements in wizard_record.partner_select:
            users_selected.append(elements.id)
        for elements in wizard_record.stage_select:
            stages_selected.append(elements.id)
        if wizard_record.partner_select:
            if wizard_record.stage_select:
                current_task = task_obj.search([('project_id', '=', name),
                                                ('user_id', 'in', users_selected),
                                                ('stage_id', 'in', stages_selected)])

            else:
                current_task = task_obj.search([('project_id', '=', name),
                                                ('user_id', 'in', users_selected)])

        else:
            if wizard_record.stage_select:
                current_task = task_obj.search([('project_id', '=', name),
                                                ('stage_id', 'in', stages_selected)])
            else:
                current_task = task_obj.search([('project_id', '=', name)])
        vals = []
        for i in current_task:
            vals.append({
                'name': i.name,
                'user_id': i.user_id.name if i.user_id.name else '',
                'stage_id': i.stage_id.name,
            })
        print(vals, 'vals')

        sheet = workbook.add_worksheet("Project Report")
        format1 = workbook.add_format({'font_size': 22, 'bg_color': '#D3D3D3'})
        format4 = workbook.add_format({'font_size': 22})
        format2 = workbook.add_format({'font_size': 12, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        format7 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        format6 = workbook.add_format({'font_size': 22, 'bg_color': '#FFFFFF'})
        format7.set_align('center')
        sheet.merge_range('A1:B1', user_obj.company_id.name, format5)
        sheet.merge_range('A2:B2', user_obj.company_id.street, format5)
        sheet.write('A3', user_obj.company_id.city, format5)
        sheet.write('B3', user_obj.company_id.zip, format5)
        sheet.merge_range('A4:B4', user_obj.company_id.state_id.name, format5)
        sheet.merge_range('A5:B5', user_obj.company_id.country_id.name, format5)
        sheet.merge_range('C1:H5', "", format5)
        sheet.merge_range(5, 0, 6, 1, "Project  :", format1)
        sheet.merge_range(5, 2, 6, 7, current_task[0].project_id.name, format1)
        sheet.merge_range('A8:B8', "Project Manager    :", format5)
        sheet.merge_range('C8:D8', current_task[0].project_id.user_id.name, format5)
        date_start = ''
        date_end = ''
        if current_task[0].project_id.date_start:
            date_start = str(current_task[0].project_id.date_start)
        if current_task[0].project_id.date:
            date_end = str(current_task[0].project_id.date)
        sheet.merge_range('A9:B9', "Start Date              :", format5)
        sheet.merge_range('C9:D9', date_start, format5)
        sheet.merge_range('A10:B10', "End Date                :", format5)
        sheet.merge_range('C10:D10', date_end, format5)
        sheet.merge_range(0, 2, 4, 5, "", format5)
        sheet.merge_range(1, 6, 4, 7, "", format5)
        sheet.merge_range(7, 4, 9, 7, "", format5)

        sheet.merge_range(10, 4, 11, 7, "", format5)
        sheet.merge_range('A11:H12', 'Open Tasks', format4)

        sheet.merge_range('A13:D13', "Tasks", format2)
        sheet.merge_range('E13:F13', "Assigned", format2)
        sheet.merge_range('G13:H13', "Stage", format2)
        row_number = 13
        column_number = 0
        for val in vals:
            sheet.merge_range(row_number, column_number, row_number, column_number+3, val['name'], format3)
            sheet.merge_range(row_number, column_number+4, row_number, column_number+5, val['user_id'], format3)
            sheet.merge_range(row_number, column_number+6, row_number, column_number+7, val['stage_id'], format3)
            row_number += 1
        
        row_number += 1
        sheet.merge_range(row_number, 0, row_number, 1, user_obj.company_id.phone, format7)
        sheet.merge_range(row_number, 2, row_number, 4, user_obj.company_id.email, format7)
        sheet.merge_range(row_number, 5, row_number, 7, user_obj.company_id.website, format7)




