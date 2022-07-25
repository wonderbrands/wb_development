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

class Picking(models.Model):
    _inherit = 'stock.picking'

    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')
    # leadtime = fields.Integer(string='Leadtime', help='Tiempo de entrega estimado del proveedor')

