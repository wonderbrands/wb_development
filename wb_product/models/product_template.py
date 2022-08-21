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

    #Product Measurements
    product_length = fields.Float(string='Largo producto', help="Largo del Producto en centimentros")
    product_height = fields.Float(string='Alto producto', help="Alto del Producto en centimentros")
    product_width = fields.Float(string='Ancho producto', help="Ancho del Producto en centimentros")
    product_weight = fields.Float(string='Peso producto', help="Peso del Producto en centimentros")
    #Packaging Measurements
    packing_length = fields.Float(string='Largo empaque', help="Largo del Empaque en centimentros")
    packing_height = fields.Float(string='Alto empaque', help="Alto del Empaque en centimentros")
    packing_width = fields.Float(string='Ancho empaque', help="Ancho del Empaque en centimentros")
    packing_weight = fields.Float(string='Peso empaque', help="Peso del Empaque en centimentros")
    #buyer = fields.One2many('usr.comprador', inverse_name='partner_id', string='Comprador responsable', help="Comprador responsable del SKU")
    buyer = fields.Many2one('res.partner', string='Comprador responsable', help='Establece el comprador encargado de este SKU')
    owner = fields.Many2one('res.partner', string='Owner comercial', help='Establece el comercial responsable de este SKU')
    #Logistics
    marketplace_codes = fields.Char(string='Códigos por marketplace', help='Códigos para comunicación con marketplace')
    provider_codes = fields.Char(string='Códigos por proveedor', help='Códigos del proveedor por SKU')
    nacional_import = fields.Selection([('importado', 'Importado'),
                                        ('nacional', 'Nacional')],
                                       string='Importacion/Nacional', help="Indica si el producto es importado o nacional")
    sold_out_industry = fields.Boolean(string='Agotado de industria', help='Producto que el proveedor reporta como agotado')
    approx_date_arrival = fields.Date(string='Fecha aprox de llegada', help='Posible fecha de resurtido por parte del proveedor para agotados de industria')
    #Product Status
    status = fields.Many2one('product.estatus', string='Estatus', help='Estatus del producto')
    substatus = fields.Many2one('product.subestatus', string='Subestatus', help='Subestatus del producto')
    #Seasonal and Period
    start_period = fields.Char(string='Inicio del periodo', help='Fecha/Mes en que inicia una estación o un Periodo para un SKU')
    end_period = fields.Char(string='Fin del periodo', help='Fecha/Mes en que finaliza una estación o un Periodo para un SKU')
    #Planning
    clasificacion_abc = fields.Char(string='Clasificación abc', help='Clasificación desarrollada por Planning')
    first_entry_date = fields.Date(string='Fecha primera entrada')
    last_entry_date = fields.Date(string='Fecha última entrada')
    first_departure_date = fields.Date(string='Fecha primera salida')
    last_departure_date = fields.Date(string='Fecha última salida')
    grava_iva = fields.Selection([('si', 'Si'),
                                  ('no', 'No')],
                                 string='Grava IVA', help='Identifica si el producto grava IVA')
    last_cost = fields.Float(string='Costo anterior', help='Muestra el costo anterior del producto', compute='_last_cost')
    replacement_cost = fields.Float(string='Costo reposición', help='Muestra el costo de reposición del producto', compute='_replacement_cost')
    last_entry_cost = fields.Float(string='Costo última entrada', help='Muestra el costo de la última entrada del producto al inventario', compute='_previous_cost')
    ps_cost = fields.Float(string='Costo PP', help="Campo con costo pronto pago. Aplica para descuentos financieros por pago")
    minimal_amount = fields.Float(string='Cantidad mínima', help='Cantidad de compra mínima por producto')
    #Logistics Scheme
    amazon_sch = fields.Many2one('esquema.logistico', string='Esquema Amazon', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    claro_sch = fields.Many2one('esquema.logistico', string='Esquema Claro Shop', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    linio_sch = fields.Many2one('esquema.logistico', string='Esquema Linio', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    meli_sch = fields.Many2one('esquema.logistico', string='Esquema Mercado Libre', help="Mapea por sku el esquema logístico (FBA/FBM/Drop/Bajo pedido/Inactivo)")
    #Categories by Marketplace
    amazon_category = fields.Many2one('cat.amazon', string='Categoría Amazon')
    claro_category = fields.Many2one('cat.claro', string='Categoría Claro Shop')
    coppel_category = fields.Many2one('cat.coppel', string='Categoría Coppel')
    elenas_category = fields.Many2one('cat.elenas', string='Categoría Elenas')
    elektra_category = fields.Many2one('cat.elektra', string='Categoría Elektra')
    linio_category = fields.Many2one('cat.linio', string='Categoría Linio')
    liverpool_category = fields.Many2one('cat.liverpool', string='Categoría Liverpool')
    meli_category = fields.Many2one('cat.meli', string='Categoría Mercado Libre')
    sears_category = fields.Many2one('cat.sears', string='Categoría Sears')
    shopee_category = fields.Many2one('cat.shopee', string='Categoría Shopee')
    vivia_category = fields.Many2one('cat.vivia', string='Categoría Vivia')
    walmart_category = fields.Many2one('cat.walmart', string='Categoría Walmart')
    web_category = fields.Many2one('cat.web', string='Categoría Web')
    #Substitute, Mirror and Variants
    substitute = fields.One2many('prod.relacionado', inverse_name='product_id', string='Productos', help='Muestra un producto que podría sustituir o reemplazar al seleccionado')
    #Stock
    stock_real = fields.Integer(string="Stock Real", compute='_total', help='muestral el stock real')
    stock_exclusivas = fields.Integer(string="Stock Exclusivas", help='Muestra el stock de exclusivas')
    stock_urrea = fields.Integer(string="Stock Urrea", help='Muestra el stock de Urrea')
    stock_markets = fields.Integer(string="Stock Markets", help='Muestra el stock en markets')
    stock_supplier = fields.Integer(string="Stock Proveedor", help='Muestra el stock del proveedor')
    #Location
    location_hallway = fields.Char(string="Pasillo")
    location_level = fields.Char(string="Nivel")
    location_area = fields.Char(string="Zona")
    location_box = fields.Char(string="Caja")

    @api.depends('seller_ids')
    def _previous_cost(self):
        self.ensure_one()

        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code != '':
            product_search = self.env['product.product'].search([('default_code', '=', self.default_code)], limit=1)
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)

            if len(all_seller_ids) <= 1:
                self.last_entry_cost = 0.0
            else:
                if all_seller_ids:
                    id_ultimo_costo = all_seller_ids[-1]
                    supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                    self.last_entry_cost = supplier.price
                    _logger.info('Costo anterior: %s', self.last_entry_cost)

                    if self.last_entry_cost == 0.0:
                        id_ultimo_costo = all_seller_ids[-2]
                        supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        self.last_entry_cost = supplier.price
                        _logger.info('Costo anterior: %s', self.last_entry_cost)

                        if self.last_entry_cost == 0.0:
                            id_ultimo_costo = all_seller_ids[-3]
                            supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                            self.last_entry_cost = supplier.price
                            _logger.info('Costo anterior: %s', self.last_entry_cost)
                        else:
                            _logger.info('Registro [-3] no es igual a 0.0')
                    else:
                        _logger.info('Registro [-3] no es igual a 0.0')
                else:
                    self.last_entry_cost = 0.0

    @api.depends('seller_ids')
    def _last_cost(self):
        self.ensure_one()

        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code != '':
            product_search = self.env['product.product'].search([('default_code', '=', self.default_code)], limit=1)
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)

            if len(all_seller_ids) <= 1:
                self.last_cost = 0.0
            else:
                if all_seller_ids:
                    id_ultimo_costo = all_seller_ids[-1]
                    supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                    self.last_cost = supplier.price
                    _logger.info('Costo ultimo: %s', self.last_cost)

                    if self.last_cost == 0.0:
                        id_ultimo_costo = all_seller_ids[-2]
                        supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        self.last_cost = supplier.price
                        _logger.info('Costo ultimo: %s', self.last_cost)

                        if self.last_cost == 0.0:
                            id_ultimo_costo = all_seller_ids[-3]
                            supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                            self.last_cost = supplier.price
                            _logger.info('Costo ultimo: %s', self.last_cost)
                        else:
                            _logger.info('Registro [-3] no es igual a 0.0')
                    else:
                        _logger.info('Registro [-2] no es igual a 0.0')
                else:
                    self.last_cost = 0.0

    @api.depends('seller_ids')
    def _replacement_cost(self):
        self.ensure_one()

        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code != '':
            product_search = self.env['product.product'].search([('default_code', '=', self.default_code)], limit=1)
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)

            if len(all_seller_ids) <= 1:
                self.replacement_cost = 0.0
            else:
                if all_seller_ids:
                    id_ultimo_costo = all_seller_ids[-1]
                    supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                    self.replacement_cost = supplier.price
                    _logger.info('Costo ultimo: %s', self.replacement_cost)

                    if self.replacement_cost == 0.0:
                        id_ultimo_costo = all_seller_ids[-2]
                        supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                        self.replacement_cost = supplier.price
                        _logger.info('Costo ultimo: %s', self.replacement_cost)

                        if self.replacement_cost == 0.0:
                            id_ultimo_costo = all_seller_ids[-3]
                            supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                            self.replacement_cost = supplier.price
                            _logger.info('Costo ultimo: %s', self.replacement_cost)
                        else:
                            _logger.info('Registro [-3] no es igual a 0.0')
                    else:
                        _logger.info('Registro [-2] no es igual a 0.0')
                else:
                    self.replacement_cost = 0.0

    #Function that prints the ZPL label of the SKU
    def print_zpl(self):
        _logger = logging.getLogger(__name__)

        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")

        dato = self
        content = ''

        for record in self:
            content += '^XA' + '\n'
            content += '^CFA,40' + '\n'
            content += '^FO15,60^FD' + str(record.default_code) + '^FS' + '\n'
            content += '^CFA,30' + '\n'
            content += '^FO15,100^FD' + str(record.name) + '^FS' + '\n'
            content += '^FO15,140^FD' + "PASILLO:" + str(record.location_hallway) + "NIVEL:" + str(
                record.location_level) + "PARED:" + str(record.location_area) + "CAJA:" + str(
                record.location_box) + '^FS' + '\n'
            content += '^FO15,180^FD' + str(fecha) + '^FS' + '\n'
            content += '^BY4,3,100' + '\n'
            content += '^FO45,240^BC^FD' + str(record.barcode) + '^FS' + '\n'
            content += '^Xz'

            headers = {'Content-Type': 'application/json'}
            # content_base64 = base64.encodestring(content.encode('utf-8'))
            b = content.encode("UTF-8")
            content_base64 = base64.b64encode(b)

            _logger.info('content_base64: %s ', content_base64)
            data = '{\n"printerId": "69183018",\n "title": "Prueba de Impresion",\n "contentType": "raw_base64",\n  "content":' + str(
                content_base64)[1:].replace("'", '"') + ',\n  "source": "Odoo Product Label ZPL"\n }'
            _logger.info('data: %s ', data)
            response = requests.post('https://api.printnode.com/printjobs', headers=headers, data=data,
                                     auth=('JClDsEj9_8tbYVQ_9C6kZ8CSi8HydNWYcvcg_KuQZQo', ''))
            _logger.info('Respuesta PrintNode: %s ', response.text)

            # raise Warning("Etiqueta ZPL creada")
        return self.write({
            'txt_filename': str(record.default_code) + '.zpl',
            'txt_binary': base64.encodestring(content.encode('utf-8'))
        })