# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests

class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    precio_min_proveedor = fields.Float(string='Precio min', help='Precio mínimo por proveedor')
    precio_max_proveedor = fields.Float(string='Precio max', help='Precio máximo por proveedor')

    minimo_compra = fields.Float(string='Monto min compra', help='Monto de compra mínimo por proveedor')