from email.policy import default

from odoo import models, fields, api
    
class UserInheritDashboard(models.Model):
    _inherit = 'res.users'
    default_dashboard = fields.Many2one('wb_data.dashboards_list', string='Default Dashboard')

class GroupInheritDashboard(models.Model):
    _inherit = 'res.groups'
    default_dashboard = fields.Many2one('wb_data.dashboards_list', string='Default Dashboard')

class GraphExceptions(models.Model):
    _name = 'wb_data.graph_exception_list'
    title = fields.Char(string='Exception rule')
    users = fields.Many2many('res.users', string='Users')
    groups = fields.Many2many('res.groups', string='Groups')
    dashboard = fields.Many2one('wb_data.dashboards_list', string='Dashboard')

class Dashboard(models.Model):
    _name = 'wb_data.dashboards_list'
    title = fields.Char(string="Dashboard Title")
    users = fields.Many2many('res.users', string='Users')
    groups = fields.Many2many('res.groups', string='Groups')
    description = fields.Text(string='Description')
    graph_exceptions = fields.Many2many('wb_data.graph_exception_list', string='Graph Exceptions')
    components = fields.One2many('wb_data.components_list', 'dashboard', string='Components')

class GraphType(models.Model):
    _name = 'wb_data.graph_type_list'
    name = fields.Char(string='Graph Type')
    js_framework = fields.Selection(
        selection=[
            ("d3js", "D3.js"),
            ("graphjs", "Graph.js")
        ],
        string="JS Framework"
    )

class Parameters(models.Model):
    _name = 'wb_data.parameters_list'
    name = fields.Char(string='Parameter Name')
    type = fields.Selection(
        selection=[
            ("string", "String"),
            ("number", "Number"),
            ("date", "Date"),
            ("datetime", "Data Time")
            ("boolean", "Boolean")
        ],
        string="Field type"
    )
    component = fields.Many2one('wb_data.components_list', string='Component')

class Component(models.Model):
    _name = 'wb_data.components_list'
    dashboard = fields.Many2one('wb_data.dashboards_list', string='Dashboard')
    title = fields.Char(string='Component Title')
    data_source_path = fields.Char(string='Data Source Path')
    data_source_type = fields.Char(string='Data Source Type')
    is_realtime = fields.Boolean(string='Realtime')
    graph_type = fields.Many2one('wb_data.graph_type_list', string='Graph Type')
    parameters = fields.One2many('wb_data.parameters_list', 'component', string='Parameters')


