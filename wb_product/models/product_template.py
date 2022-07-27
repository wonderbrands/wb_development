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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #Medidas de Producto
    largo_producto = fields.Float(string='Largo producto', help="Largo del Producto en centimentros")
    alto_producto = fields.Float(string='Alto producto', help="Alto del Producto en centimentros")
    ancho_producto = fields.Float(string='Ancho producto', help="Ancho del Producto en centimentros")
    peso_producto = fields.Float(string='Peso producto', help="Peso del Producto en centimentros")
    #Medidas de Empaque
    largo_empaque = fields.Float(string='Largo empaque', help="Largo del Empaque en centimentros")
    alto_empaque = fields.Float(string='Alto empaque', help="Alto del Empaque en centimentros")
    ancho_empaque = fields.Float(string='Ancho empaque', help="Ancho del Empaque en centimentros")
    peso_empaque = fields.Float(string='Peso empaque', help="Peso del Empaque en centimentros")
    comprador = fields.One2many('usr.comprador', inverse_name='partner_id', string='Comprador responsable', help="Comprador responsable del SKU")
    #Logística
    codigos_marketplace = fields.Char(string='Códigos por marketplace', help='Códigos para comunicación con marketplace')
    codigos_proveedor = fields.Char(string='Códigos por proveedor', help='Códigos del proveedor por SKU')
    importacion_nacional = fields.Selection([('importado', 'Importado'),
                                             ('nacional', 'Nacional')],
                                            string='Importacion/Nacional', help="Indica si el producto es importado o nacional")
    agotado_industria = fields.Boolean(string='Agotado de industria', help='Producto que el proveedor reporta como agotado')
    fecha_aprox_llega = fields.Date(string='Fecha aprox de llegada', help='Posible fecha de resurtido por parte del proveedor para agotados de industria')
    #Estatus del producto
    subestatus_act = fields.Selection([('resurtible', 'Resurtible'),
                                       ('agotado', 'Agotado de industria'),
                                       ('nocompetitivo', 'No competitivo'),
                                       ('noresurtible', 'No resurtible')],
                                      string='Sub estatus A', help='Sub estatus del producto si el éste se encuentra Activo, reactivado o desarchivado')
    subestatus_des = fields.Selection([('proveedor', 'Descontinuado por proveedor'),
                                       ('rotacion', 'Descontinuado por rotación'),
                                       ('competitivo', 'No competitivo')],
                                      string='Sub estatus B', help='Sub estatus del producto si éste se encuentra Inactivo o por proximidad baja')
    prod_active = fields.Boolean(string='Activo', help='Muestra si el producto está en estatus de Reactivado')
    prod_reactivated = fields.Boolean(string='Reactivado', help='Muestra si el producto está en estatus de Reactivado')
    prod_unarchived = fields.Boolean(string='Archivado', help='Muestra si el producto está en estatus de Desarchivado')
    prod_inactive = fields.Boolean(string='Inactivo', help='Muestra si el producto está en estatus de Inactivo')
    prod_low_proximity = fields.Boolean(string='Prox baja', help='Muestra si el producto está en estatus de Proximidad Baja')


    #@api.onchange('estatus_act','estatus_des')
    def _estatus(self):
        self.ensure_one()

        estatus = self.estatus_act
        estado = self.active

        if estado == False:
            self.archivo = True
        if estatus == 'inactivo':
            self.inactivo = True
            self.estatus_des = 'desarchivo'
        if estatus == 'proxbaja':
            self.prox_baja = True
            self.estatus_des = 'reactivo'


    fecha_prim_entrada = fields.Date(string='Fecha primera entrada')
    fecha_ulti_entrada = fields.Date(string='Fecha última entrada')
    fecha_prim_salid = fields.Date(string='Fecha primera salida')
    fecha_ulti_salid = fields.Date(string='Fecha última salida')
    grava_iva = fields.Selection([('si', 'Si'),
                                  ('no', 'No')],
                                 string='Grava IVA', help='Identifica si el producto grava IVA')
    costo_anterior = fields.Float(string='Costo anterior', help='Muestra el costo anterior del producto', compute='_costo_anterior')
    costo_reposicion = fields.Float(string='Costo reposición', help='Muestra el costo de reposición del producto', compute='_costo_reposicion')
    costo_ultimo = fields.Float(string='Costo última entrada', help='Muestra el costo de la última entrada del producto al inventario', compute='_costo_ultimo')
    monto_minimo = fields.Float(string='Cantidad mínima', help='Cantidad de compra mínima por producto')

    #Estacionales y Periodo
    fecha_inicio = fields.Char(string='Inicio del periodo', help='Fecha/Mes en que inicia una estación o un Periodo para un SKU')
    fecha_fin = fields.Char(string='Fin del periodo', help='Fecha/Mes en que finaliza una estación o un Periodo para un SKU')

    #Planning
    clasificacion_abc = fields.Char(string='Clasificación abc', help='Clasificación desarrollada por Planning')

    #Esquema Logístico
    esq_amazon = fields.Many2one('esquema.logistico', string='Esquema Amazon', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    esq_claro = fields.Many2one('esquema.logistico', string='Esquema Claro Shop', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    esq_linio = fields.Many2one('esquema.logistico', string='Esquema Linio', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    esq_meli = fields.Many2one('esquema.logistico', string='Esquema Mercado Libre', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")

    #Categorías por Marketplace
    categoria_amazon = fields.Many2one('cat.amazon', string='Categoría Amazon')
    categoria_claro = fields.Many2one('cat.claro', string='Categoría Claro Shop')
    categoria_coppel = fields.Many2one('cat.coppel', string='Categoría Coppel')
    categoria_elenas = fields.Many2one('cat.elenas', string='Categoría Elenas')
    categoria_elektra = fields.Many2one('cat.elektra', string='Categoría Elektra')
    categoria_linio = fields.Many2one('cat.linio', string='Categoría Linio')
    categoria_liverpool = fields.Many2one('cat.liverpool', string='Categoría Liverpool')

    categoria_meli = fields.Many2one('cat.meli', string='Categoría Mercado Libre')
    categoria_sears = fields.Many2one('cat.sears', string='Categoría Sears')
    categoria_shopee = fields.Many2one('cat.shopee', string='Categoría Shopee')
    categoria_vivia = fields.Many2one('cat.vivia', string='Categoría Vivia')
    categoria_walmart = fields.Many2one('cat.walmart', string='Categoría Walmart')
    categoria_web = fields.Many2one('cat.web', string='Categoría Web')

    #Sustituto, Espejo y Variantes
    sustituto = fields.One2many('prod.relacionado', inverse_name='product_id', string='Productos')

    @api.depends('seller_ids')
    def _costo_anterior(self):
        self.ensure_one()

        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code != '':
            product_search = self.env['product.product'].search([('default_code', '=', self.default_code)], limit=1)
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)

            if len(all_seller_ids) <= 1:
                self.costo_anterior = 0.0
            else:
                if all_seller_ids:
                    id_ultimo_costo = all_seller_ids[-2]
                    supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                    self.costo_anterior = supplier.price
                    _logger.info('Costo anterior: %s', self.costo_anterior)

                    if self.costo_anterior == 0.0:
                        id_ultimo_costo = all_seller_ids[-3]
                        supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        self.costo_anterior = supplier.price
                        _logger.info('Costo anterior: %s', self.costo_anterior)

                        if self.costo_anterior == 0.0:
                            id_ultimo_costo = all_seller_ids[-4]
                            supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                            self.costo_anterior = supplier.price
                            _logger.info('Costo anterior: %s', self.costo_anterior)
                        else:
                            _logger.info('Registro [-3] no es igual a 0.0')
                    else:
                        _logger.info('Registro [-3] no es igual a 0.0')
                else:
                    self.costo_anterior = 0.0

    @api.depends('seller_ids')
    def _costo_ultimo(self):
        self.ensure_one()

        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code != '':
            product_search = self.env['product.product'].search([('default_code', '=', self.default_code)], limit=1)
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)

            if len(all_seller_ids) <= 1:
                self.costo_ultimo = 0.0
            else:
                if all_seller_ids:
                    id_ultimo_costo = all_seller_ids[-1]
                    supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                    self.costo_ultimo = supplier.price
                    _logger.info('Costo ultimo: %s', self.costo_ultimo)

                    if self.costo_ultimo == 0.0:
                        id_ultimo_costo = all_seller_ids[-2]
                        supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        self.costo_ultimo = supplier.price
                        _logger.info('Costo ultimo: %s', self.costo_ultimo)

                        if self.costo_ultimo == 0.0:
                            id_ultimo_costo = all_seller_ids[-3]
                            supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                            self.costo_ultimo = supplier.price
                            _logger.info('Costo ultimo: %s', self.costo_ultimo)
                        else:
                            _logger.info('Registro [-3] no es igual a 0.0')
                    else:
                        _logger.info('Registro [-2] no es igual a 0.0')
                else:
                    self.costo_ultimo = 0.0

    @api.depends('seller_ids')
    def _costo_reposicion(self):
        self.ensure_one()

        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code != '':
            product_search = self.env['product.product'].search([('default_code', '=', self.default_code)], limit=1)
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)

            if len(all_seller_ids) <= 1:
                self.costo_reposicion = 0.0
            else:
                if all_seller_ids:
                    id_ultimo_costo = all_seller_ids[-1]
                    supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                    self.costo_reposicion = supplier.price
                    _logger.info('Costo ultimo: %s', self.costo_reposicion)

                    if self.costo_reposicion == 0.0:
                        id_ultimo_costo = all_seller_ids[-2]
                        supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        self.costo_reposicion = supplier.price
                        _logger.info('Costo ultimo: %s', self.costo_reposicion)

                        if self.costo_reposicion == 0.0:
                            id_ultimo_costo = all_seller_ids[-3]
                            supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                            self.costo_reposicion = supplier.price
                            _logger.info('Costo ultimo: %s', self.costo_reposicion)
                        else:
                            _logger.info('Registro [-3] no es igual a 0.0')
                    else:
                        _logger.info('Registro [-2] no es igual a 0.0')
                else:
                    self.costo_reposicion = 0.0

    #@api.depends('seller_ids')
    #def _costo_anterior(self):
    #    self.ensure_one()