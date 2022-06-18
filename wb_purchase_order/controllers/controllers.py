# -*- coding: utf-8 -*-
# from odoo import http


# class WbPurchaseOrder(http.Controller):
#     @http.route('/wb_purchase_order/wb_purchase_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_purchase_order/wb_purchase_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_purchase_order.listing', {
#             'root': '/wb_purchase_order/wb_purchase_order',
#             'objects': http.request.env['wb_purchase_order.wb_purchase_order'].search([]),
#         })

#     @http.route('/wb_purchase_order/wb_purchase_order/objects/<model("wb_purchase_order.wb_purchase_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_purchase_order.object', {
#             'object': obj
#         })
