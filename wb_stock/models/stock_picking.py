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

    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')#, compute='make_invisible', store=True)
    # leadtime = fields.Integer(string='Leadtime', help='Tiempo de entrega estimado del proveedor')
    invisible_field = fields.Boolean(string='Es IN?', help='Un campo de ayuda al programador para saber si el movimiento de almacén es un IN')

    @api.depends('invisible_field')
    def make_invisible(self):
        self.ensure_one()
        #for each in self:
        type_id = self.picking_type_id.id
        print(type_id)
        if type_id == 1:
            print(self.name)
            self.invisible_field = True
        else:
            self.invisible_field = False

