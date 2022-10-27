# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
import logging
import json
import requests
from io import StringIO, BytesIO

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    #Fechas proveedor
    leadtime = fields.Integer(related='partner_id.leadtime' ,string='Leadtime', help='Tiempo de entrega estimado del proveedor')
    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')#, compute='_fecha_cita')
    fecha_prevista = fields.Datetime(string='Fecha prevista', compute='_fecha_prevista')

    #Relacionados
    monto_minimo = fields.Char(related='partner_id.monto_minimo', string='Mínimo de compra', help='Mínimo de compra por proveedor')
    unidad = fields.Selection([('pza', 'Piezas'),
                               ('doc', 'Docenas'),
                               ('caj', 'Cajas'),
                               ('pes', 'Pesos')], string='Unidad', related='partner_id.unidad')
    dias_credito = fields.Integer(related='partner_id.dias_credito', string='Días de crédito', help='Días de crédito que otorga el proveedor')
    dias_compra = fields.Char(related='partner_id.dias_compra', string='Días de compra', help='Días en los que se le puede enviar pedido al proveedor')

    pedido_original = fields.Float(string='Pedido Original', help='Indica la cantidad demandada original')

    supplier = fields.Boolean(related='partner_id.supplier', string='¿Es proveedor?')

    def _fecha_cita(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)

        stock_pick = self.env['stock.picking'].search([('origin', '=', self.name)])

        if self.incoming_picking_count:

            for each in stock_pick:
                picking_type = each.picking_type_id.ids
                picking_date = each.fecha_cita_almc
                picking_name = each.name

                _logger.info('picking_type: %s', picking_type)
                _logger.info('picking_date: %s', picking_date)
                _logger.info('picking_name: %s', picking_name)

                for rec in picking_type:
                    if rec == 1:
                        self.fecha_cita_almc = picking_date
                        _logger.info('El picking_type_id es 1')
                    else:
                        self.fecha_cita_almc = ''
                        _logger.info('El picking_type_id es diferente de 1 ')
        else:
            self.fecha_cita_almc = ''

    def _fecha_prevista(self):
        fecha_crea = self.create_date
        lead = self.leadtime

        if fecha_crea:
            fecha = fecha_crea + relativedelta(days = lead)
            self.fecha_prevista = fecha
        else:
            self.fecha_prevista = ''