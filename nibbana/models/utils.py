import logging
import uuid
from odoo import fields

logger = logging.getLogger(__name__)


def generate_uid(obj):
    return '{}'.format(uuid.uuid4().hex)


def increment_metric(obj, code, name):
    metric = obj.env['nibbana.metric_counter'].search([
        ('owner','=',obj.env.user.id),
        ('code','=', code),
        ('metric_date','=', fields.Date.today())
    ])
    if metric:
        metric.value += 1
    else:
        metric = obj.env['nibbana.metric_counter'].create({
            'owner': obj.env.user.id,
            'name': name,
            'code': code,
            'metric_date': fields.Date.today(),
            'value': 1
        })



def decrement_metric(obj, code, name):
    metric = obj.env['nibbana.metric_counter'].search([
        ('owner','=',obj.env.user.id),
        ('code','=', code),
        ('metric_date','=', fields.Date.today())
    ])
    if metric:
        if metric.value > 0:
            metric.value -= 1
    else:
        # Create empty metric
        metric = obj.env['nibbana.metric_counter'].create({
            'owner': obj.env.user.id,
            'name': name,
            'code': code,
            'metric_date': fields.Date.today(),
            'value': 0
        })
