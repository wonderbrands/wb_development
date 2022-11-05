# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests
from io import StringIO, BytesIO

class ResPartner(models.Model):
    _inherit = "res.partner"

    monto_minimo = fields.Char(string='Mínimo de compra', help='Mínimo de compra por proveedor')
    dias_credito = fields.Integer(string='Días de crédito', help='Días de crédito que da el proveedor')
    dias_compra = fields.Char(string='Días de compra', help='Días en los que se le puede enviar pedido al proveedor')

    unidad = fields.Selection([('pza', 'Piezas'),
                               ('doc', 'Docenas'),
                               ('caj', 'Cajas'),
                               ('pes', 'Pesos')], string='Unidad')

    leadtime = fields.Integer(string='Leadtime', help='Tiempo de entrega estimado del proveedor')
    supplier = fields.Boolean(string='¿Es proveedor?', help='Marca si el usuario de compra es un Proveedor')