from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = 'product.template'

    # Nuevos campos Male

    security_stock = fields.Integer(string="Stock de seguridad", help='Muestra el stock de seguridad')
    visualization_stock = fields.Integer(string="Stock de visualización de canal", help='Muestra el stock de visualización de canal')
    pvp_aim = fields.Float(string='PVP objetivo', help='Muestra el PVP objetivo')
    purchase_frequency = fields.Integer(string="Frecuencia de compra", help='Muestra la frecuencia de compra')
    pc1 = fields.Float(string='PC1', help='Muestra el PC1')
    pc2 = fields.Float(string='PC3', help='Muestra el PC3')
    cluster = fields.Char(string='Cluster', help='Muestra el cluster')
    loading_qty_ = fields.Integer(string="Loading qty", help='Loading qty')

    # Campo Male 23-oct-2024
    data_inventory_date = fields.Datetime(string='Fecha de inventario', help='Establece la fecha del inventario')

    # Campo Male 10-dic-2024
    data_supplier_code = fields.Char(string='Proveedor', help='Código del proveedor')