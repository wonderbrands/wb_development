# -*- coding: utf-8 -*-
# from odoo import http


# class WbStock(http.Controller):
#     @http.route('/wb_stock/wb_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_stock/wb_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_stock.listing', {
#             'root': '/wb_stock/wb_stock',
#             'objects': http.request.env['wb_stock.wb_stock'].search([]),
#         })

#     @http.route('/wb_stock/wb_stock/objects/<model("wb_stock.wb_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_stock.object', {
#             'object': obj
#         })
