# -*- coding: utf-8 -*-
import logging
import json
from odoo import http

_logger = logging.getLogger(__name__)


class SmartScreenshots(http.Controller):
    @http.route('/smart_screenshots/ping/', type='json', auth='public', methods=['POST'])
    def ping(self):
        request = http.request.httprequest.data.decode('utf-8')
        data = json.loads(request)
        if data == {'data': 'ping'}:
            return {'status': 'pong'}
        return {'status': 'error'}

    @http.route('/smart_screenshots/tasks/', type='json', auth='public',  methods=['POST'])
    def post_task_screenshots(self):
        data_decode = http.request.httprequest.data.decode('utf-8')
        _logger.debug(data_decode)
        data = json.loads(data_decode)
        task = http.request.env['project.task'].sudo().create({
                'name': 'screenshot Task',
                'user_id': http.request.uid,
            })
        for value in data.values():
            attachment = http.request.env['ir.attachment'].sudo().create({
                'name': value['filename'],
                'datas_fname': 'screenshot.png',
                'type': 'binary',
                'datas': value['data'].encode('utf-8'),
                'res_model': 'project.task',
                'res_id': task.id,
                'mimetype': 'image/png',
            })

            project_task_screenshot = http.request.env['project.task.screenshot'].sudo().create({
                'name': value['filename'],
                'problem_task_id': task.id,
                'image': value['data'].encode('utf-8'),
                'source_url': value['page_url'],
                'attachment_id': attachment.id,
                'type': 'problem',
            })
        return {'status': 'ok'}

    @http.route('/smart_screenshots/tasks/', type='json', auth='public', methods=['PUT'])
    def put_task_screenshots(self):
        data_decode = http.request.httprequest.data.decode('utf-8')
        data = json.loads(data_decode)
        if 'task_id' in data:
            task_id = data.pop('task_id')
            task = http.request.env['project.task'].sudo().browse(task_id)
            if task:
                for value in data.values():
                    attachment = http.request.env['ir.attachment'].sudo().create({
                        'name': value['filename'],
                        'datas_fname': 'screenshot.png',
                        'type': 'binary',
                        'datas': value['data'].encode('utf-8'),
                        'res_model': 'project.task',
                        'res_id': task.id,
                        'mimetype': 'image/png',
                    })

                    project_task_screenshot = http.request.env['project.task.screenshot'].sudo().create({
                        'name': value['filename'],
                        'image': value['data'].encode('utf-8'),
                        'source_url': value['page_url'],
                        'attachment_id': attachment.id,
                        'type': value.get('type', 'problem'),
                    })
                    if value.get('type', 'problem') == 'problem':
                        project_task_screenshot.problem_task_id = task.id
                    else:  # type == 'solution'
                        project_task_screenshot.solution_task_id = task.id
        return {'status': 'ok'}
