# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):

    _inherit = 'project.task'

    product_ids = fields.Many2many('product.product', string="Products")
