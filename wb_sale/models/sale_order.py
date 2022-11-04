# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
from pytz import timezone
import logging
import json
import requests

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    availability = fields.Boolean(string='Disponibilidad', help='Venta negada o cancelada por disponibilidad')
    delivery_time = fields.Boolean(string='Tiempo de entrega', help='Venta negada o cancelada por tiempo de entrega')
    sale_price = fields.Boolean(string='Precio de venta', help='Venta negada o cancelada por precio de venta')
    other = fields.Boolean(string='Otra', help='Venta negada o cancelada por una razón que no se encuentra en el listado')
    message = fields.Text(string='¿Cuál es el motivo?', help='Anote la razón por la cual se negó o canceló la venta', track_visibility=True)
    time_zone = fields.Datetime(string='Zona horaria', help='Prueba de la zona horaria')

    auto_invoiced = fields.Boolean(string='Fue autofacturado', help='Muestra si la SO activa fue facturada de manera automática')

    @api.onchange('other')
    def _clear_field(self):

        if not self.other:
            self.message = False