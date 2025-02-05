from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class DashboardData(http.Controller):
    @http.route('/wb_cycle_count/table', type='json', auth='user')
    def dashboard_data(self):
        _logger.info("==========================")
        _logger.info(request.jsonrequest)
        _logger.info("==========================")

