from odoo import models, fields, api, _

class ResPartnerRES(models.Model):
    _inherit = "res.partner"

    advance_payment_date = fields.Integer(string='Día de pago de anticipo', help='Cantidad de días de pago de anticipo')
    percent_supplier_advance = fields.Float(string='% Anticipo proveedor', help='Muestra el porcentaje de anticipo al proveedor')
    lt_ag_channel = fields.Integer(string='LT AGcanal', help='LT AGcanal')