# -*- coding: utf-8 -*-
# from odoo import http


# class WbSaleOrder(http.Controller):
#     @http.route('/wb_sale_order/wb_sale_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_sale_order/wb_sale_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_sale_order.listing', {
#             'root': '/wb_sale_order/wb_sale_order',
#             'objects': http.request.env['wb_sale_order.wb_sale_order'].search([]),
#         })

#     @http.route('/wb_sale_order/wb_sale_order/objects/<model("wb_sale_order.wb_sale_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_sale_order.object', {
#             'object': obj
#         })
