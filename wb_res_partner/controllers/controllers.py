# -*- coding: utf-8 -*-
# from odoo import http


# class WbResPartner(http.Controller):
#     @http.route('/wb_res_partner/wb_res_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_res_partner/wb_res_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_res_partner.listing', {
#             'root': '/wb_res_partner/wb_res_partner',
#             'objects': http.request.env['wb_res_partner.wb_res_partner'].search([]),
#         })

#     @http.route('/wb_res_partner/wb_res_partner/objects/<model("wb_res_partner.wb_res_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_res_partner.object', {
#             'object': obj
#         })
