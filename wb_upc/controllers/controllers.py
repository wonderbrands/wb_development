# -*- coding: utf-8 -*-
# from odoo import http


# class WbUpc(http.Controller):
#     @http.route('/wb_upc/wb_upc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_upc/wb_upc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_upc.listing', {
#             'root': '/wb_upc/wb_upc',
#             'objects': http.request.env['wb_upc.wb_upc'].search([]),
#         })

#     @http.route('/wb_upc/wb_upc/objects/<model("wb_upc.wb_upc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_upc.object', {
#             'object': obj
#         })
