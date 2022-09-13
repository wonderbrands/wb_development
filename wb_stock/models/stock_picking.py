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

    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')#, compute='make_invisible')
    # leadtime = fields.Integer(string='Leadtime', help='Tiempo de entrega estimado del proveedor')
    invisible_field = fields.Boolean(string='Es Pick?', help='Un campo de ayuda al programador para saber si el movimiento de almacén es un PICK')

    def make_invisible(self):
        name = self.name
        if 'AG/PICK/' in str(name):
            self.invisible_field = False
        else:
            self.invisible_field = True

