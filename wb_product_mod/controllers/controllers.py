# -*- coding: utf-8 -*-
# from odoo import http


# class WbProductTemplate(http.Controller):
#     @http.route('/wb_product_template/wb_product_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_product_template/wb_product_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_product_template.listing', {
#             'root': '/wb_product_template/wb_product_template',
#             'objects': http.request.env['wb_product_template.wb_product_template'].search([]),
#         })

#     @http.route('/wb_product_template/wb_product_template/objects/<model("wb_product_template.wb_product_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_product_template.object', {
#             'object': obj
#         })
