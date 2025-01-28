from odoo import http
from odoo.http import request


class AvailableDashboards(http.Controller):
    @http.route('/wb_data/available_dashboards', type='json', auth='user')
    def available_dashboards(self):
        #GET GROUPS OF THE USER
        groups = request.env.user.groups_id
        user = request.env.user

        #GET DEFAULT DASHBOARD FOR THE USER
        default_dashboard = user.default_dashboard
        #IF THE USER DOESN'T HAVE A DEFAULT DASHBOARD,
        #GET THE DEFAULT DASHBOARD OF ONE OF THE GROUPS
        if not default_dashboard:
            for group in groups:
                default_dashboard = group.default_dashboard
                if default_dashboard:
                    break

        #GET DASHBOARDS FOR THE GROUPS OR THE USER, EXCLUDE THE EXCEPTIONS
        dashboards = request.env['wb_data.dashboards_list'].search([
            '|',
            ('groups', 'in', groups.ids),
            ('users', 'in', user.id),
        ])

        #GET DASHBOARDS EXCEPTIONS
        exceptions = request.env['wb_data.graph_exception_list'].search([
            ('groups', 'in', groups.ids),
            ('users', 'in', user.ids),
        ])

        #GET DASHBOARDS EXCEPT THE EXCEPTIONS
        #dashboards = dashboards - [exception.dashboard for exception in exceptions]

        return {
            'dashboards': [
                {
                    'id': dashboard.id,
                    'title': dashboard.title,
                    'default': dashboard.id == default_dashboard.id
                } for dashboard in dashboards
            ],
        }