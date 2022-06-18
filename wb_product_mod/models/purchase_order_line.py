# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    pedido_original = fields.Float(string='Pedido Original', help='Indica la cantidad demandada original')