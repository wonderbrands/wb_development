from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class DashboardData(http.Controller):
    @http.route('/wb_data/get_dashboard', type='json', auth='user')
    def dashboard_data(self):
        try:
            dashboard_name = request.jsonrequest["name"]
        except:
            return {
                "status": "error",
                "error_code": "You need to specify which dashboard are you querying"
            }

        #GET THE DASHBOARD NAME
        dashboard = request.env["wb_data.dashboards_list"].search(
            [
                ("title", "=", dashboard_name)
            ],
            limit=1
        )

        if not dashboard:
            return {
                "status": "error",
                "error_code": "No dashboard with that name"
            }

        return {
            "status": "success",
            "dashboard_data":{
                "name": dashboard.title,
                "components": [
                    {
                        "title": component.title,
                        "data_source_type": component.data_source_type.name,
                        "data_source_path": component.data_source_path,
                        "is_realtime": component.is_realtime,
                        "graph_type": component.graph_type.name,
                        "css": component.css,
                        "parameters": [
                            {
                                "name": parameter.name,
                                "type": parameter.type,
                                "default": parameter.default if not parameter.code_interpreted_default else parameter.execute(parameter.default),
                                "available_values": [value.value for value in parameter.options]
                            } for parameter in component.parameters
                        ]
                    } for component in dashboard.components
                ]
            }
        }