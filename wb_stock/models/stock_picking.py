# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests
import re
from io import StringIO, BytesIO

class Picking(models.Model):
    _inherit = 'stock.picking'

    fecha_cita_almc = fields.Datetime(string='Fecha cita en almacén')#, compute='make_invisible', store=True)
    # leadtime = fields.Integer(string='Leadtime', help='Tiempo de entrega estimado del proveedor')
    invisible_field = fields.Boolean(string='Es IN?', help='Un campo de ayuda al programador para saber si el movimiento de almacén es un IN')
    restocked = fields.Boolean(
        string="Is restocked?",
        default=False
    )
    
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


    def reservation_from_superior_lvs(self):
        pattern = re.compile(r"(AG/Stock/TL/N|AG/Stock/N)([0-9]|[1-9][0-9]|100)\b")
        locations = [location.complete_name for location in self.env["stock.location"].search([
            '&',
            ('usage', '=', 'internal'),  
            '|',
            ('complete_name', 'ilike', 'AG/Stock/TL/N'),
            ('complete_name', 'ilike', 'AG/Stock/N')
        ]) if pattern.match(location.complete_name)]
        locations.sort(reverse=True)
        products = self.move_ids_without_package
        prods_witho_stock = []
        for product in products:
            demand_qty = product.product_uom_qty
            product_quantities = self.env["stock.quant"].search([
                ("product_id", "=", product.product_id.id), 
                ("location_id.complete_name", "in", locations)
            ], order="location_id desc")
            print(f"Initially needed {product.product_id.name}: {product.product_uom_qty}")
            total_available = sum(quant.quantity - quant.reserved_quantity for quant in product_quantities)
            if total_available < demand_qty:
                prods_witho_stock.append(product.product_id.name)
                continue  
            for quant in product_quantities:
                available_qty = quant.quantity - quant.reserved_quantity
                print(f"{product.product_id.name}: Available {available_qty} in {quant.location_id.complete_name}")
                if available_qty <= 0:
                    continue
                needed = min(available_qty, demand_qty)
                demand_qty -= needed
                print(f"Needed {needed}, taken from {quant.location_id.complete_name}. Remaining demand: {demand_qty}.")
                self.env["stock.move.line"].create({
                    "picking_id": self.id,
                    "product_id": product.product_id.id,
                    "location_id": quant.location_id.id,
                    "product_uom_id": product.product_uom.id,
                    "qty_done": needed,
                    "location_dest_id": self.location_dest_id.id,
                    "state": "assigned",
                })
                if demand_qty <= 0:
                    break
        if self.state not in ["assigned", "confirmed"]:
            self.action_assign()
        for move_line in self.move_line_ids:
            if move_line.qty_done == 0:
                move_line.qty_done = move_line.product_uom_qty
        try:
            for move in self.move_ids_without_package:
                if move.state != "done":
                    move._action_done()
            self.action_done()
            print(f"Picking {self.name} successfully closed.")
        except Exception as e:
            print(f"Failed to close picking {self.name}: {e}")
        if prods_witho_stock:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Stock insuficiente",
                    'type': 'danger',
                    'message': f"Los siguientes productos no tienen stock suficiente: {', '.join(prods_witho_stock)}",
                    'sticky': True,
                }
            }

