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
    sub_product_line_ids = fields.One2many(related='bom_ids.bom_line_ids', string='Componentes', readonly=True)
    is_kit = fields.Boolean(string='Es un kit?', help='Este campo estará marcado si el SKU es combo o tiene lista de materiales', compute='_is_kit')
    component_list = fields.Boolean(string='Lista de componentes', help='Este campo estará marcado si el SKU es combo o tiene lista de materiales', compute='_id_yuju_kit')
    combo_qty = fields.Float(string='Total combos', help='Muestra la cantidad de combos que se pueden realizar con la lista de materiales actual', compute='_total_combos')
    #Calculated measures
    is_calculated_combo = fields.Boolean(string='Es combo', compute='calculated_measures')
    calculated_weight = fields.Float(string='Peso calculado', help='Muestra el cálculo del peso de los componentes del combo en kilogramos')
    calculated_volume = fields.Float(string='Volumen calculado', help='Muestra el cálculo del volumen de los componentes del combo, transforma centimetros cúbicos a Litros')

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

    #@api.depends('is_kit')
    def _total_combos(self):
        if self.bom_count > 0 and self.yuju_kit:
            bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.yuju_kit.id)])
            for each in bom_line_ids:
                combo_calculation = each.combo_qty
                self.combo_qty = combo_calculation
        else:
            self.combo_qty = 0.0

    #@api.onchange('yuju_kit')
    def _id_yuju_kit(self):
        bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.yuju_kit.id)])
        self.component_list = True
        self.sub_product_line_ids = bom_line_ids

    #Calcula el peso y volumen para combos
    def calculated_measures(self):
        if self.bom_count > 0:
            weight_measures = []
            length_measures = []
            height_measures = []
            width_measures = []
            volume_calculation = []
            bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.yuju_kit.id)])
            product_ids = bom_line_ids['product_id']
            for product in product_ids:
                #Peso
                weight = product['packing_weight']
                weight_measures.append(weight)
                #Largo
                length = product['packing_length']
                length_measures.append(length)
                #Alto
                height = product['packing_height']
                height_measures.append(height)
                #Ancho
                width = product['packing_width']
                width_measures.append(width)

            max_length = max(length_measures)
            max_height = max(height_measures)
            sum_width = sum(width_measures)
            self.calculated_volume =  (max_length * max_height * sum_width) / 1000
            self.calculated_weight = sum(weight_measures)
            self.is_calculated_combo = True
        else:
            self.is_calculated_combo = False