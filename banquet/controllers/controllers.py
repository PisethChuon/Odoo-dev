# -*- coding: utf-8 -*-
# from odoo import http


# class Banquet(http.Controller):
#     @http.route('/banquet/banquet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/banquet/banquet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('banquet.listing', {
#             'root': '/banquet/banquet',
#             'objects': http.request.env['banquet.banquet'].search([]),
#         })

#     @http.route('/banquet/banquet/objects/<model("banquet.banquet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('banquet.object', {
#             'object': obj
#         })

