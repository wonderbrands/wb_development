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

class ESQLogistico(models.Model):
    _name = 'esquema.logistico'
    _description = 'Catalogo de categorías Amazon'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class USRComprador(models.Model):
    _name = 'usr.comprador'
    _description = 'Comprador Responsable del SKU'

    partner_id = fields.Integer(string='id', readonly=True)
    name = fields.Many2one('res.partner', string='Comprador')
    kam = fields.Many2one('res.partner', string='KAM')

class PRODRelacionado(models.Model):
    _name = 'prod.relacionado'

    product_id = fields.Integer(string='id', readonly=True)
    name_sus = fields.Many2one('product.product', string='Producto Sustituto')
    name_mir = fields.Many2one('product.product', string='Producto Espejo')

class InternalCategory(models.Model):
    _name = "internal.category"
    _description = "Modelo que incluye un catálogo de categorías internas para el Owner y Comprador"

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Modelo para creación de marcas de producto"

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    supplier = fields.Many2one('res.partner', string='Proveedor')