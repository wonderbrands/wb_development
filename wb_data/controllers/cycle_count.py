from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class DashboardData(http.Controller):
    @http.route('/wb_cycle_count/table', type='json', auth='user')
    def dashboard_data(self):
        _logger.info("==========================")
        _logger.info(request.jsonrequest)
        _logger.info("==========================")

        logs = request.env["wb_cycle_count.log"].search([
            ("scanned_at", ">=", request.jsonrequest["Desde"]),
            ("scanned_at", "<=", request.jsonrequest["Hasta"]),
            ("session.name", "=", request.jsonrequest["Wave"])  # Assuming session has a `name` field
        ])

        return {
            "columnNames": ["Producto", 
            "Ubicación", 
            "Cantidad", 
            "Estatus", 
            "Ola"],
            "rows": [
                [
                    log.product.name,
                    log.zone.name,
                    log.qty,
                    log.status,
                    log.session.name
                ] for log in logs
            ]
        }

