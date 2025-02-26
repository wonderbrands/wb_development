from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class FieldsLog(models.Model):
    _name = "wb_log.log"
    _rec_name = "link_2_rec" 

    record = fields.Char(
        string = "Record"
    )
    
    rec_id = fields.Char(
        string = "ID"
    )

    model = fields.Many2one(
        comodel_name = "ir.model",
        string = "Model",
    )

    field = fields.Many2one(
        comodel_name = "ir.model.fields",
        string = "Field",
    )
    
    user = fields.Many2one(
        comodel_name = "res.users",
        string = "Done by"
    )

    at = fields.Datetime(
        string = "Done at"
    )

    prev_value = fields.Char(
        string = "Previous Value"
    )

    new_value = fields.Char(
        string = "Next value"
    )

    movment_type = fields.Selection(
        string = "Movment type",
        selection = [
            ("created", "Created"),
            ("updated", "Updated"),
            ("deleted", "Deleted or archived")
        ]
    )

    link_2_rec = fields.Html(
        string = "Record",
        compute='_compute_record'
    )

    @api.depends('record', 'model', 'rec_id')
    def _compute_record(self):
        for record in self:
            if record.record and record.model and record.rec_id:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                url = f"<a href=\"{base_url}/web#id={record.rec_id}&model={record.model.model}\">{record.record}</a>"
                #_logger.info("***********************************")
                #_logger.info(url)
                #_logger.info("***********************************")
                record.link_2_rec = url
            else: 
                record.link_2_rec = False
                return False
