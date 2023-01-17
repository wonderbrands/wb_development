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
    product_weight = fields.Float(string='Peso producto', help="Peso del Producto en kilogramos")
    product_volume = fields.Float(string='Volumen producto', help="Volumen del Producto", compute='_volumen')
    #Packaging Measurements
    packing_length = fields.Float(string='Largo empaque', help="Largo del Empaque en centimentros")
    packing_height = fields.Float(string='Alto empaque', help="Alto del Empaque en centimentros")
    packing_width = fields.Float(string='Ancho empaque', help="Ancho del Empaque en centimentros")
    packing_weight = fields.Float(string='Peso empaque', help="Peso del Empaque en centimentros")
    #Comercial
    #buyer = fields.One2many('usr.comprador', inverse_name='partner_id', string='Comprador responsable', help="Comprador responsable del SKU")
    buyer = fields.Many2one('res.partner', string='Comprador responsable', help='Establece el comprador encargado de este SKU')
    owner = fields.Many2one('res.partner', string='Owner comercial', help='Establece el comercial responsable de este SKU')
    internal_category = fields.Many2one('internal.category', string='Categoría interna', help='Categoría interna para el equipo de SR')
    brand = fields.Many2one('product.brand', string='Marca', help='Marca a la que pertecene el SKU')
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
    substatus = fields.Many2one('product.subestatus', string='Subestatus', help='Subestatus del producto')#, domain=[('status_subsequence', "=", 'status_sequence')])
    status_sequence = fields.Char(related='status.sequence', string='Secuencia')
    status_subsequence = fields.Char(related='substatus.subsequence', string='Subsecuencia')
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
    #Costs
    previous_cost = fields.Float(related='product_variant_id.previous_cost', string='Costo anterior', help='Muestra el costo anterior del producto')
    replacement_cost = fields.Float(string='Costo reposición', help='Muestra el costo de reposición del producto', compute='_replacement_cost')
    last_entry_cost = fields.Float(string='Costo última entrada', help='Muestra el costo de la última entrada del producto al inventario', compute='_last_cost')
    ps_cost = fields.Float(string='Costo PP', help="Campo con costo pronto pago. Aplica para descuentos financieros por pago")
    minimal_amount = fields.Float(string='Cantidad mínima', help='Cantidad de compra mínima por producto')
    #Logistic Scheme
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
    stock_real = fields.Integer(related='product_variant_id.stock_real', string="Stock Real", help='muestral el stock real')#, compute='_total')
    stock_exclusivas = fields.Integer(related='product_variant_id.stock_exclusivas', string="Stock Exclusivas", help='Muestra el stock de exclusivas')
    stock_urrea = fields.Integer(related='product_variant_id.stock_urrea', string="Stock Urrea", help='Muestra el stock de Urrea')
    stock_markets = fields.Integer(related='product_variant_id.stock_markets', string="Stock Markets", help='Muestra el stock en markets')#, compute='_min_stock_markets')
    stock_supplier = fields.Integer(related='product_variant_id.stock_supplier', string="Stock Proveedor", help='Muestra el stock del proveedor')
    stock_mercadolibre = fields.Integer(related='product_variant_id.stock_mercadolibre', string="Stock mercado Libre", readonly=False)#, compute='_total')
    stock_linio = fields.Integer(related='product_variant_id.stock_linio', string="Stock Linio", readonly=False)#, compute='_total')
    stock_amazon = fields.Integer(related='product_variant_id.stock_amazon', string="Stock Amazon", readonly=False)#, compute='_total')
    #Location
    location_hallway = fields.Char(string="Pasillo")
    location_level = fields.Char(string="Nivel")
    location_area = fields.Char(string="Zona")
    location_box = fields.Char(string="Caja")
    #Label
    txt_filename = fields.Char()
    txt_binary = fields.Binary("Etiqueta ZPL")
    #Markets
    mlm_ventas = fields.Char(string='Somos Reyes Ventas', help='Código MLM del SKU perteneciente a ventas')
    mlm_oficiales = fields.Char(string='Somos Reyes Oficiales', helpp='Código MLM del SKU perteneciente a oficiales')
    stock_full_ventas = fields.Integer(string='Stock Full Ventas', help='Stock de ventas')
    stock_full_oficiales = fields.Integer(string='Stock Full Oficiales', help='Stock de oficiales')
    full_api_ventas = fields.Boolean(string='Fullfilment Ventas API', help='Esquema del SKU de ventas mapeado por API')
    full_api_oficiales = fields.Boolean(string='Fullfilment Oficiales API', help='Esquema del SKU de oficiales mapeado por API')
    #Markets Manual
    full_ventas = fields.Boolean(string='Fullfilment Ventas', help='Esquema del SKU de ventas mapeado de forma manual')
    full_oficiales = fields.Boolean(string='Fullfilment Oficiales', help='Esquema del SKU de oficiales mapeado de forma manual')

    # Function that prints the previous cost
    @api.depends('seller_ids')
    def _previous_cost(self):
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

    # Function that prints the last cost
    @api.depends('seller_ids')
    def _last_cost(self):
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

    #Function that prints the replacement cost
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

    #Function that print the actual stock
    @api.depends('stock_exclusivas', 'stock_urrea')
    def _total(self):
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

    #Function that print the actual stock
    @api.depends('stock_real')
    def _min_stock_markets(self):
        self.ensure_one()
        try:
            # --- Adecuacion para cuando el producto es un combo "is_kit=True"
            _logger = logging.getLogger(__name__)
            lista_stock_markets = []
            lista_stock_real = []
            stock_markets = 0
            stock_subproducto = 0

            default_code = self.default_code
            _logger.info('default_code: %s', default_code)
            product_is_kit = self.env['product.product'].search([('default_code', '=', default_code)])#.is_kit
            # _logger.info('product_is_kit: %s', str(product_is_kit) )
            if product_is_kit:
                sub_product_line_ids = self.env['product.product'].search([('default_code', '=', default_code)]).sub_product_line_ids
                # _logger.info('sub_product_line_ids: %s', str(sub_product_line_ids) )
                for sub_product_line_id in sub_product_line_ids:
                    id_sub_product = sub_product_line_id.id
                    _logger.info('id_sub_product: %s', str(id_sub_product))
                    product_id = self.env['sub.product.lines'].search([('id', '=', id_sub_product)]).product_id.id
                    product_quantity = self.env['sub.product.lines'].search([('id', '=', id_sub_product)]).quantity
                    # _logger.info('product_id: %s,  PRODUCT CUANTITY: %s', str(product_id), str(product_quantity) )

                    stock_markets_subproductos = self.env['product.product'].search(
                        [('id', '=', product_id)]).stock_markets

                    # -- para los combos cuando vienen varios productos
                    stock_real_subproducto = int(int(
                        self.env['product.product'].search([('id', '=', product_id)]).stock_real) / product_quantity)

                    stock_exclusivas_subproducto = self.env['product.product'].search(
                        [('id', '=', product_id)]).stock_exclusivas
                    stock_urrea_subproducto = self.env['product.product'].search([('id', '=', product_id)]).stock_urrea

                    if stock_markets_subproductos <= 0:
                        stock_subproducto_markets = stock_real_subproducto + stock_exclusivas_subproducto + stock_urrea_subproducto
                    else:
                        stock_subproducto_markets = stock_markets_subproductos

                    # _logger.info('stock_markets: %s', stock_subproducto_markets  )
                    # _logger.info('stock_real_subproducto: %s', str(stock_real_subproducto) )

                    lista_stock_markets.append(stock_subproducto_markets)
                    lista_stock_real.append(stock_real_subproducto)
                # Cual es ma lenor cantidad
                # _logger.info('lista_stock_markets: %s', str(lista_stock_markets) )
                stock_minimo_markets = min(lista_stock_markets)
                stock_minimo_real = min(lista_stock_real)
                self.stock_markets = stock_minimo_markets
                self.stock_real = stock_minimo_real
            # --- Termina Adecuacion

        except Exception as e:
            _logger.info('ERROR _min_stock_markets(): | %s', str(e))

    #Function that print VAT price
    @api.depends('list_price')
    def _price_vat(self):
        self.ensure_one()
        if self.list_price:
            self.vat_price = round(float(self.list_price)*1.16, 0)
        else:
            self.vat_price=0.00

    #Function that print the volume of product
    @api.depends('product_width', 'product_height', 'product_length')
    def _volumen(self):
        _logger = logging.getLogger(__name__)
        for rec in self:
            if rec.product_width > 0 and rec.product_height > 0 and rec.product_length > 0:
                rec.product_volume = round((rec.product_width * rec.product_height * rec.product_length) / 5000, 2)
            else:
                rec.product_volume = 0.00
