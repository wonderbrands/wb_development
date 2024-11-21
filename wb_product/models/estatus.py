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

class ProdEstatus(models.Model):
    _name = 'product.estatus'
    _description = 'Estatus de producto'

    name = fields.Char(string='Nombre')
    sequence = fields.Char(string='Secuencia asignada')

class ProdSubestatus(models.Model):
    _name = 'product.subestatus'
    _description = 'Subestatus de producto'

    name = fields.Char(string='Nombre')
    subsequence = fields.Char(string='Subsecuencia asignada')