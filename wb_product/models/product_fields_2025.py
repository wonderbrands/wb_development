# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    target_items = fields.Integer(
        string='Goal sales',
    )

    purchase_active = fields.Boolean(
        string='Restockable',
    )

    variant = fields.Char(
        string='Variant',
    )


    