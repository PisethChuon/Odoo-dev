# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class basic_server_side(models.Model):
#     _name = 'basic_server_side.basic_server_side'
#     _description = 'basic_server_side.basic_server_side'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

