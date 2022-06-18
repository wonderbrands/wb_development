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

class CATAmazon(models.Model):
    _name = 'cat.amazon'
    _description = 'Catalogo de categorías Amazon'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATClaro(models.Model):
    _name = 'cat.claro'
    _description = 'Catalogo de categorías ClaroShop'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATCoppel(models.Model):
    _name = 'cat.coppel'
    _description = 'Catalogo de categorías Coppel'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATElektra(models.Model):
    _name = 'cat.elektra'
    _description = 'Catalogo de categorías Elektra'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATElenas(models.Model):
    _name = 'cat.elenas'
    _description = 'Catalogo de categorías Elenas'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATLinio(models.Model):
    _name = 'cat.linio'
    _description = 'Catalogo de categorías Linio'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATLiverpool(models.Model):
    _name = 'cat.liverpool'
    _description = 'Catalogo de categorías Liverpool'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATMeli(models.Model):
    _name = 'cat.meli'
    _description = 'Catalogo de categorías Mercado Libre'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATSears(models.Model):
    _name = 'cat.sears'
    _description = 'Catalogo de categorías Sears'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATShopee(models.Model):
    _name = 'cat.shopee'
    _description = 'Catalogo de categorías Shopee'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATVivia(models.Model):
    _name = 'cat.vivia'
    _description = 'Catalogo de categorías Vivia'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATWalmart(models.Model):
    _name = 'cat.walmart'
    _description = 'Catalogo de categorías Walmart'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')

class CATWeb(models.Model):
    _name = 'cat.web'
    _description = 'Catalogo de categorías Web'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')