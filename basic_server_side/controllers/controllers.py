# -*- coding: utf-8 -*-
# from odoo import http


# class BasicServerSide(http.Controller):
#     @http.route('/basic_server_side/basic_server_side', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/basic_server_side/basic_server_side/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('basic_server_side.listing', {
#             'root': '/basic_server_side/basic_server_side',
#             'objects': http.request.env['basic_server_side.basic_server_side'].search([]),
#         })

#     @http.route('/basic_server_side/basic_server_side/objects/<model("basic_server_side.basic_server_side"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('basic_server_side.object', {
#             'object': obj
#         })

