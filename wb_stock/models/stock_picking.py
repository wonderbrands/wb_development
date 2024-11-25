# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import json
import requests
import re
from io import StringIO, BytesIO

class Picking(models.Model):
    _inherit = 'stock.picking'

    fecha_cita_almc = fields.Datetime(
        string='Fecha cita en almacén'
    )
    invisible_field = fields.Boolean(
        string='Es IN?', 
        help='Un campo de ayuda al programador para saber si el movimiento de almacén es un IN'
    )
    restocked_field = fields.Boolean(
        string="Is restocked?",
        default=False
    )
    show_full_button = fields.Boolean(
        string="Show full button",
        compute='_compute_show_full_button',
    )

    @api.depends('state', 'restocked_field')
    def _compute_show_full_button(self):
        """
        Compute whether to show the "Full" button based on the picking's state and restocked status.
        """
        for picking in self:
            picking.show_full_button = picking.state in ['waiting', 'confirmed'] and picking.restocked_field

    @api.depends('invisible_field')
    def make_invisible(self):
        """
        Compute the value of the invisible field based on the picking type.
        """
        self.ensure_one()
        picking_type_id = self.picking_type_id.id
        self.invisible_field = picking_type_id == 1

    def reservation_from_superior_lvs(self):
        # Define location pattern and retrieve internal locations
        location_pattern = re.compile(r"(AG/Stock/TL/N|AG/Stock/N)([0-9]|[1-9][0-9]|100)\b")
        locations = [location.complete_name for location in self.env["stock.location"].search([
            '&',
            ('usage', '=', 'internal'),  
            '|',
            ('complete_name', 'ilike', 'AG/Stock/TL/N'),
            ('complete_name', 'ilike', 'AG/Stock/N')
        ]) if location_pattern.match(location.complete_name)]
        locations.sort(reverse=True)

        # Retrieve products to be processed
        products = self.move_ids_without_package
        insufficient_stock_products = []

        # Process each product in the picking
        for product in products:
            demand_qty = product.product_uom_qty
            product_quants = self.env["stock.quant"].search([
                ("product_id", "=", product.product_id.id),
                ("location_id.complete_name", "in", locations)
            ], order="location_id desc")

            logging.info(f"Processing product {product.product_id.name}. Quantity needed: {demand_qty}")

            # Calculate total available quantity
            total_available = sum(quant.quantity - quant.reserved_quantity for quant in product_quants)

            if total_available < demand_qty:
                logging.warning(f"Not enough stock for {product.product_id.name}. Total available: {total_available}")
                insufficient_stock_products.append(product.product_id.name)
                continue

            # Reserve quantities from eligible locations
            for quant in product_quants:
                available_qty = quant.quantity - quant.reserved_quantity
                if available_qty <= 0:
                    continue

                reserve_qty = min(available_qty, demand_qty)
                demand_qty -= reserve_qty

                logging.info(f"Reserving {reserve_qty} of {product.product_id.name} from {quant.location_id.complete_name}. "
                            f"Remaining demand: {demand_qty}")

                # Create stock move line for reserved quantity
                self.env["stock.move.line"].create({
                    "picking_id": self.id,
                    "product_id": product.product_id.id,
                    "location_id": quant.location_id.id,
                    "product_uom_id": product.product_uom.id,
                    "qty_done": 0,  # Ensure the product is only reserved
                    "location_dest_id": self.location_dest_id.id,
                    "state": "assigned",
                    "product_uom_qty": reserve_qty,
                })

                # Update the reserved quantity on the quant
                quant.reserved_quantity += reserve_qty

                if demand_qty <= 0:
                    break

        # Mark picking as ready
        self.action_assign()

        # Notify user about products with insufficient stock
        if insufficient_stock_products:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Insufficient Stock",
                    'type': 'danger',
                    'message': f"The following products could not be fully reserved: {', '.join(insufficient_stock_products)}",
                    'sticky': True,
                }
            }
