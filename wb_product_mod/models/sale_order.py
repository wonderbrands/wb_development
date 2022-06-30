# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    disponibilidad = fields.Boolean(string='Disponibilidad', help='Venta negada por disponibilidad')
    tiempo_entrega = fields.Boolean(string='Tiempo de entrega', help='Venta negada por tiempo de entrega')
    precio_venta = fields.Boolean(string='Precio de venta', help='Venta negada por precio de venta')