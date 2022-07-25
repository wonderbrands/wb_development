# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests

class ProductProduct(models.Model):
    _inherit = "product.product"

    upc = fields.Char(string='UPC code', size=12)

    def generate_upc(self, cr, uid, ids, context=None):
        upc_code = self.pool.get('upc.generator').generate_upc(cr, uid, ids)
        self.write(cr, uid, ids, {'upc': upc_code})
        return True

product_product()