from odoo import models, fields, api

class WatchedFields(models.Model):
    _name = "wb_log.watched_fields"

    model = fields.Many2one(
        comodel = "ir.model",
        string = "Model",
        required = True
    )

    field = fields.Many2one(
        comodel = "ir.model_fields",
        string = "Field",
        required = True,
    )

    check_when_create = fields.Boolean(
        string = "Log when create"
    )

    check_when_update = fields.Boolean(
        string = "Log when update"
    )

    check_when_remove = fields.Boolean(
        string = "Log when remove or archive"
    )



    @api.onchange('model')
    def _onchange_model(self):
        """Dynamically set the domain for 'field' based on the selected model"""
        if self.model:
            return {'domain': {'field': [('model_id', '=', self.model.id)]}}
        return {'domain': {'field': []}}
