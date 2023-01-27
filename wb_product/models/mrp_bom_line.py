# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests


class MrpBomLineComponent(models.Model):
    _name = 'mrp.bom.line.component'
    _description = 'Bill of Material Line'

    #Stock
    product_id = fields.Integer(string='Id', readonly=True)
    product = fields.Many2one('product.product', string='Componente', readonly=True)
    stock_qty = fields.Integer(string='Stock', help='Muestra el stock del producto', readonly=True)#, compute='_bom_lines')
    combo_qty = fields.Float(string='Costo Revisado', help='Muestra la cantidad de combos que se pueden realizar con la lista de materiales actual', readonly=True)#, compute='_stock')

    #---Funcion de calculo adicionado por somos-reyes
    @api.depends('stock_qty')
    def _stock(self):
        _logger = logging.getLogger(__name__)
        min_stock = []
        for each in self:
            product = each.env['product.product'].search([('id', '=', each.product_id.id)], limit=1)
            #self.quantity_virtual_available = product.virtual_available
            each.stock_qty = product.stock_real
            min_stock.append(each.stock_qty)
            #print(min_stock)
        min_amount = min(min_stock, default=0)
        #print('Cantidad mínima de la lista: ')
        #print(min_amount)
        #total_combos = min_amount / self.product_qty
        self.combo_qty = min_amount