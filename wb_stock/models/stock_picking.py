# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests

class Picking(models.Model):
    _inherit = 'stock.picking'

    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')#, compute='make_invisible', store=True)
    # leadtime = fields.Integer(string='Leadtime', help='Tiempo de entrega estimado del proveedor')
    invisible_field = fields.Boolean(string='Es IN?', help='Un campo de ayuda al programador para saber si el movimiento de almacén es un IN')

    # Dev for new picking process
    pick_priority = fields.Selection([('0', '0'), ('1', '1'), ('2', '2')],
                             default='0', string='Priority level', help='Field that allows to enter the priority level of pick', store=True)
    pick_zone = fields.Many2one('stock.location', string='Pick zone', help='Field that allows to choose a stock location, this field is set from the first line of the stock move line', compute='_zone_assignment', index=True,store=True) #Campo relacionado con el modelo de Ubicaciones
    priority_check = fields.Boolean(string='Priority check', help='This field will be set "True" once it has been checked by the script')
    is_colecta = fields.Boolean(string='Es colecta', help='Campo que nos permite saber si este Pick es de Mercado Libre colecta')

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

    def _zone_assignment(self):
        for rec in self:
            if 'PICK' in rec.name:
                if rec.move_line_ids_without_package:
                    move_id = rec.move_line_ids_without_package.location_id.location_id.ids
                    print('ID del primer movimiento de almacen: ', move_id)
                    rec.pick_zone = move_id[0]
                    print(rec.pick_zone)
                else:
                    rec.pick_zone = None
            else:

                rec.pick_zone = None


