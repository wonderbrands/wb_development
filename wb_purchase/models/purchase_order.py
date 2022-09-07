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
    leadtime = fields.Integer(related='partner_id.leadtime' ,string='Leadtime', help='Tiempo de entrega estimado del proveedor', readonly=False)
    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')#, compute='_fecha_cita')
    fecha_prevista = fields.Datetime(string='Fecha prevista', compute='_fecha_prevista')

    #Relacionados
    monto_minimo = fields.Char(related='partner_id.monto_minimo', string='Mínimo de compra', help='Mínimo de compra por proveedor')
    unidad = fields.Selection([('pza', 'Piezas'),
                               ('doc', 'Docenas'),
                               ('caj', 'Cajas'),
                               ('pes', 'Pesos')], string='Unidad', related='partner_id.unidad', readonly=False)
    dias_credito = fields.Integer(related='partner_id.dias_credito', string='Días de crédito', help='Días de crédito que otorga el proveedor', readonly=False)
    dias_compra = fields.Char(related='partner_id.dias_compra', string='Días de compra', help='Días en los que se le puede enviar pedido al proveedor', readonly=False)

    pedido_original = fields.Float(string='Pedido Original', help='Indica la cantidad demandada original')

    def _fecha_cita(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)

        if self.incoming_picking_count >= 1:
            fecha = self.env['stock.picking'].search([('origin', '=', self.name)])
            registry = fecha[1].name
            date = fecha[1].fecha_cita_almc
            _logger.info('Segundo %s ', registry)
            if 'IN' in registry:
                new_fecha = date
                self.fecha_cita_almc = new_fecha
            else:
                print('Fallo el stock picking')
        else:
            _logger.info('Segundo %s ')

    def _fecha_prevista(self):
        fecha_crea = self.create_date
        lead = self.leadtime

        if fecha_crea:
            fecha = fecha_crea + relativedelta(days = lead)
            self.fecha_prevista = fecha
        else:
            self.fecha_prevista = ''