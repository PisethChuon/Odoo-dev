# -*- coding: utf-8 -*-
# from odoo import http


# class BasicServerSide(http.Controller):
#     @http.route('/basic__server__side/basic__server__side', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/basic__server__side/basic__server__side/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('basic__server__side.listing', {
#             'root': '/basic__server__side/basic__server__side',
#             'objects': http.request.env['basic__server__side.basic__server__side'].search([]),
#         })

#     @http.route('/basic__server__side/basic__server__side/objects/<model("basic__server__side.basic__server__side"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('basic__server__side.object', {
#             'object': obj
#         })

