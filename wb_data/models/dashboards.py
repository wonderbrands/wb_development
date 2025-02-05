from odoo import models, fields, api
from datetime import datetime, timedelta
import logging
    

_logger = logging.getLogger(__name__)

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
    title = fields.Char(string="Dashboard Title", required=True)
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
            ("graphjs", "Graph.js"),
            ("prime_vue", "Prime Vue")
        ],
        string="JS Framework"
    )

class ParameterSelectables(models.Model):
    _name = 'wb_data.parameter_selectable'
    parameter = fields.Many2one(name="Parameter",
                                comodel_name="wb_data.parameters_list")
    value = fields.Char(name="value")


class Parameters(models.Model):
    _name = 'wb_data.parameters_list'
    name = fields.Char(string='Parameter Name')
    type = fields.Selection(
        selection=[
            ("string", "String"),
            ("number", "Number"),
            ("date", "Date"),
            ("datetime", "Datetime"),
            ("boolean", "Boolean"),
            ("selection", "Selection")
        ],
        string="Field type"
    )
    default = fields.Char(string="Default value")
    code_interpreted_default = fields.Boolean(string="Code interpreted default")
    component = fields.Many2one('wb_data.components_list', string='Component')

    def execute(self, code):
        result = eval(code)
        return result
       


    code_interpreted_selection = fields.Boolean(string="Code interpreted selection")
    selection_code = fields.Char(string="Code for selection fields")
    options = fields.One2many(string="options",
                              comodel_name='wb_data.parameter_selectable',
                              inverse_name="parameter")


    def set_options_from_code(self):
        if self.code_interpreted_selection and self.selection_code:
            try:
                result = self.execute(self.selection_code)
                self.write({'options': [(5, 0, 0)]})
                for res in result:
                    new_record = {
                        'parameter': self.id,
                        'value': res,
                    }
                    self.write({'options': [(0, 0, new_record)]})
            except Exception as e:
                _logger.error(e)
                pass

    

    @api.onchange('selection_code', 'code_interpreted_selection')
    def _define_code_options(self):
        self.set_options_from_code()
        



    """
    @api.depends('default', 'code_interpreted_default')    
    def _default_inter(self):
        for record in self:
            if record.code_interpreted_default:
                try:
                    result = this.excecute(record.default)
                except:
                    result = False
                
                record.interpreted_def = str(result)
    """

class Component(models.Model):
    _name = 'wb_data.components_list'
    dashboard = fields.Many2one('wb_data.dashboards_list', string='Dashboard')
    title = fields.Char(string='Component Title', required=True)
    data_source_path = fields.Char(string='Data Source Path', required=True)
    data_source_type = fields.Many2one("wb_data.data_source_type", string='Data Source Type', required=True)
    is_realtime = fields.Boolean(string='Realtime')
    graph_type = fields.Many2one('wb_data.graph_type_list', string='Graph Type', required=True)
    parameters = fields.One2many('wb_data.parameters_list', 'component', string='Parameters')
    css = fields.Text(string="Enclose CSS")

class DataSourceType(models.Model):
    _name = "wb_data.data_source_type"
    name = fields.Char(string="Type")