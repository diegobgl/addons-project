#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################
#
# Difusión Visual Interactivo S.L.
# Copyright (C) Difusión Visual Interactivo S.L.
# all rights reserved
# http://difusionvisual.com
# contacto@difusionvisual.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
{
    'name': 'Lead to Task',
    'version': '11.0.1.0.0',
    'summary': """Create Tasks from Leads and add count task in project""",
    'description': """Create Tasks from Leads and add count task in project""",
    'author': 'DV Interactivo',
    'company': 'DV Interactivo',
    'website': 'http://www.dvinteractivo.com',
    'category': 'Sales',
    'license': 'AGPL-3',
    'depends': [
        'crm',
        'project',
        'hr_timesheet',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/crm_lead2projecttask_wizard_view.xml',
        'views/crm_lead_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,

}
