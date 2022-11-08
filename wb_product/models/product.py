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
