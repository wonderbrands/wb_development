# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
import logging
import json
import requests

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    pedido_original = fields.Float(string='Pedido Original', help='Indica la cantidad demandada original')#, compute='_monto_minimo', inverse='_inverse_monto_minimo')
    monto_minimo = fields.Float(related='product_id.minimal_amount', string='Cantidad mínima', help='Cantidad de compra mínima por producto')

    @api.onchange('product_qty','pedido_original')
    def _monto_minimo(self):
        self.ensure_one()
        monto = self.monto_minimo

        if monto > 0:
            if self.pedido_original < monto:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _(
                            "El pedido original debe ser mayor al monto mínimo",
                            pack_name=self.product_id.name,
                            unit=self.product_uom.name
                        ),
                    },
                }
            if self.product_qty < monto:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _(
                            "La cantidad debe ser mayor al monto mínimo",
                            pack_name=self.product_id.name,
                            unit=self.product_uom.name
                        ),
                    },
                }