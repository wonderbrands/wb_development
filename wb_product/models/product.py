# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo import exceptions
from collections import defaultdict
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests


class ProductProduct(models.Model):
    _inherit = 'product.product'

    #Costs
    previous_cost = fields.Float(string='Costo anterior', help='Muestra el costo anterior del producto', compute='_product_previous_cost')
    revised_cost = fields.Float(string='Costo revisado', help='Muestra el costo a revisar por el usuario')
    #Stock
    stock_real = fields.Integer(string="Stock Real", compute='_product_total', help='muestral el stock real')
    stock_exclusivas = fields.Integer(string="Stock Exclusivas", help='Muestra el stock de exclusivas')
    stock_urrea = fields.Integer(string="Stock Urrea", help='Muestra el stock de Urrea')
    stock_markets = fields.Integer(string="Stock Markets", help='Muestra el stock en markets')#, compute='_min_stock_markets')
    stock_supplier = fields.Integer(string="Stock Proveedor", help='Muestra el stock del proveedor')
    stock_mercadolibre = fields.Integer(string="Stock mercado Libre", compute='_product_total', readonly=False)
    stock_linio = fields.Integer(string="Stock Linio", compute='_product_total', readonly=False)
    stock_amazon = fields.Integer(string="Stock Amazon", compute='_product_total', readonly=False)
    # Sub products
    sub_product_line_ids = fields.One2many('mrp.bom.line.component', inverse_name='product_id', string='Componentes')
    is_kit = fields.Boolean(string='Es un kit?', help='Este campo estará marcado si el SKU es combo o tiene lista de materiales', compute='_is_kit')
    component_lines = fields.Boolean(string='Lineas del componente', help='Este campo estará marcado si el SKU es combo o tiene lista de materiales', compute='_bom_component')
    combo_qty = fields.Float(string='Total combos', help='Muestra la cantidad de combos que se pueden realizar con la lista de materiales actual', compute='_stock')

    # Function that prints the previous cost
    @api.depends('seller_ids')
    def _product_previous_cost(self):
        #self.ensure_one()
        _logger = logging.getLogger(__name__)
        for each in self:
            if each.default_code or each.default_code != '':
                product_search = each.env['product.product'].search([('default_code', '=', each.default_code)], limit=1)
                all_seller_ids = product_search.seller_ids.ids
                _logger.info('seller_ids: %s', all_seller_ids)

                if len(all_seller_ids) < 1:
                    each.previous_cost = 0.0
                else:
                    if all_seller_ids:
                        id_ultimo_costo = all_seller_ids[-1]
                        supplier = each.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        each.previous_cost = supplier.price
                        _logger.info('Costo anterior: %s', each.previous_cost)

                        if len(all_seller_ids) > 1:
                            if each.previous_cost == 0.0:
                                id_ultimo_costo = all_seller_ids[-2]
                                supplier = each.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                                each.previous_cost = supplier.price
                                _logger.info('Costo anterior: %s', each.previous_cost)
                                if len(all_seller_ids) > 2:
                                    if each.previous_cost == 0.0:
                                        id_ultimo_costo = all_seller_ids[-3]
                                        supplier = each.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                                        each.previous_cost = supplier.price
                                        _logger.info('Costo anterior: %s', each.previous_cost)
                                    else:
                                        _logger.info('Registro [-3] no es igual a 0.0')
                            else:
                                _logger.info('Registro [-2] no es igual a 0.0')
                    else:
                        each.previous_cost = 0.0
            else:
                _logger.info('No se encontró el SKU')

    @api.depends('stock_exclusivas', 'stock_urrea')
    def _product_total(self):
        _logger = logging.getLogger(__name__)
        for each in self:
            try:
                stock_real = 0
                reserved_quantity = 0
                previsto = 0
                quantity_total = 0
                reserved_quantity_total = 0

                default_code = each.default_code
                product = each.env['product.product'].search([('default_code', '=', default_code)], limit=1)
                quants = product.stock_quant_ids
                for quant in quants:
                    quant_id = quant.id
                    location_id = quant.location_id.id
                    location = each.env['stock.location'].search([('id', '=', location_id)], limit=1)
                    location_display_name = location.display_name
                    location_name = quant.location_id.name
                    quantity = quant.quantity
                    reserved_quantity = quant.reserved_quantity
                    previsto = quantity - reserved_quantity

                    _logger.info('SR STOCK| default_code:' + str(default_code) + '|location_id:' + str(location_id) + '|location_name:' + str(location_name) + '|' + str(location_display_name) + '|quantity:' + str(quantity) + '|reserved_quantity:' + str(reserved_quantity) + '|previsto:' + str(previsto))
                    # --- Todo lo que esta en las ubicaciones AG
                    if 'AG/Stock' in str(location_display_name):
                        # stock_real += quantity
                        quantity_total = quantity_total + quantity
                        reserved_quantity_total = reserved_quantity_total + reserved_quantity
                        _logger.info('quantity_total:' + str(quantity_total) + ',reserved_quantity_total: ' + str(
                            reserved_quantity_total))

                each.stock_real = quantity_total - reserved_quantity_total

                # --- Calculando el stock para los marketplaces
                if each.stock_markets == 0:
                    each.stock_mercadolibre = each.stock_real + each.stock_exclusivas + each.stock_urrea
                else:
                    each.stock_mercadolibre = each.stock_markets

                if each.stock_mercadolibre < 0:
                    each.stock_mercadolibre = 0

                if each.stock_markets == 0:
                    each.stock_linio = each.stock_real + each.stock_exclusivas
                else:
                    each.stock_linio = each.stock_markets

                if each.stock_linio < 0:
                    each.stock_linio = 0

                if each.stock_markets == 0:
                    each.stock_amazon = each.stock_real + each.stock_exclusivas + each.stock_urrea
                else:
                    each.stock_amazon = each.stock_markets

                if each.stock_amazon < 0:
                    each.stock_amazon = 0

            except Exception as e:
                _logger.error('ODOO CALCULATE|' + str(e))

    #Function that evaluates if product is combo or kit
    @api.depends('is_kit')
    def _is_kit(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        if self.bom_count > 0:
            self.is_kit = True
        else:
            self.is_kit = False

    #---Funcion de calculo adicionado por somos-reyes
    @api.depends('is_kit')
    def _stock(self):
        _logger = logging.getLogger(__name__)
        if self.is_kit == True:
            min_stock = []
            _logger.info('ES UN COMBO')
            for each in self:
                if each.sub_product_line_ids:
                    each.component_lines = True
                    sub_product_lines = each.sub_product_line_ids.product.ids
                    for line in sub_product_lines:
                        product = each.env['product.product'].search([('id', '=', line)], limit=1)
                        stock = product.stock_real
                        min_stock.append(stock)
                        _logger.info('Array: ', min_stock)
                    min_amount = min(min_stock, default=0)
                    _logger.info('Cantidad mínima de la lista: %s', min_amount)
                    each.combo_qty = min_amount
                else:
                    each.component_lines = False
        else:
            self.component_lines = False
            _logger.info('NO ES UN COMBO')

    @api.onchange('previous_cost')
    @api.depends('is_kit')
    def _bom_component(self):
        _logger = logging.getLogger(__name__)
        exist_record = []
        #Modelo One2many
        mrp_bom_line = self.env['mrp.bom.line.component']
        if self.is_kit == True:
            _logger.info('ES UN COMBO')
            #Lista de componentes Yuju
            bom_ids = self.yuju_kit
            bom_line = bom_ids.bom_line_ids
            for bom_lines_ids in bom_line:
                if self.sub_product_line_ids:
                    self.component_lines = True
                    chk_lines = self.sub_product_line_ids.product.ids
                    product_id = bom_lines_ids.product_id.id
                    product_stock = bom_lines_ids.product_id.stock_real
                    for lines in chk_lines:
                        _logger.info('la tabla SI tiene datos')
                        _logger.info('PRIMERO SE EVALUARÁN LOS IDS PARA EVITAR CUPLICARLOS')
                        if product_id in chk_lines:
                            self.component_lines = False
                            _logger.info('Ya existe ese SKU en la tabla')
                            _logger.info('NO se va a crear ningún registro')
                        else:
                            self.component_lines = True
                            _logger.info('Este SKU NO existe en la tabla')
                            _logger.info('Se creará un nuevo registro')
                            data = {'product_id': self.id,
                                    'product': product_id,
                                    'stock_qty': product_stock,
                                    'combo_qty': 1
                                    }
                            _logger.info('SKU List: %s', data)
                            # exist_record.append(product_id)
                            mrp_bom_line.create(data)
                else:
                    self.component_lines = True
                    product_id = bom_lines_ids.product_id.id
                    product_stock = bom_lines_ids.product_id.stock_real
                    _logger.info('la tabla NO tiene datos')
                    _logger.info('SE CREARAÁN NUEVOS REGISTROS')
                    data = {'product_id': self.id,
                            'product': product_id,
                            'stock_qty': product_stock,
                            'combo_qty': 1
                            }
                    _logger.info('SKU List: %s', data)
                    # exist_record.append(product_id)
                    mrp_bom_line.create(data)
        else:
            self.component_lines = True
            _logger.info('NO ES UN COMBO')
