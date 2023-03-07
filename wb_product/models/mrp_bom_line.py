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


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    _description = 'Bill of Material Line'

    #Stock
    stock_qty = fields.Float(string='Stock', help='Muestra el stock del producto', compute='_stock')
    combo_qty = fields.Float(string='Total combos', help='Muestra la cantidad de combos que se pueden realizar con la lista de materiales actual', readonly=True)

    #---Funcion de calculo adicionado por somos-reyes
    @api.depends('stock_qty')
    def _stock(self):
        _logger = logging.getLogger(__name__)
        min_stock = []
        for each in self:
            product_qty = each.product_qty
            product = each.env['product.product'].search([('id', '=', each.product_id.id)], limit=1)
            each.stock_qty = product.stock_real
            combo_calculation = each.stock_qty / product_qty
            round_qty = round(combo_calculation)
            min_stock.append(round_qty)
        min_amount = min(min_stock, default=0)
        self.combo_qty = min_amount