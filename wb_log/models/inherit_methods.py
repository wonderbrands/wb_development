from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class WriteInLog(models.BaseModel):
    _inherit = "base"

    def _is_model_and_field_being_watched(self, 
                                          model = None, 
                                          fields = None,
                                          field = None):


        _logger.info("------------------------------")
        _logger.info(list(fields))
        _logger.info(model)
        _logger.info("------------------------------")
        if fields:
            watched_field = self.env["wb_log.watched_fields"].search(
                [
                    ("model.model", "=", model),
                    ("field.name", "in", list(fields))
                ]
            )
            return {
                "is_watched": not len(watched_field)==0,
                "fields": watched_field
            }
        if field:
            watched_field = self.env["wb_log.watched_fields"].search(
                [
                    ("model.name", "=", model),
                    ("field.name", "=", field)
                ]
            )
            return {
                "is_watched": not len(watched_field)==0,
                "field": watched_field
            }

    def _write_log(self,
                   model, 
                   field, 
                   record,  
                   prev_val, 
                   next_val, 
                   operation_type,
                   rec_id):

        self.env["wb_log.log"].create(    
            {
                "record": str(record),
                "model": str(model),
                "field": field,
                "user": self.env.user.id,
                "at": datetime.now(),
                "prev_value": str(prev_val),
                "new_value": str(next_val),
                "movment_type": operation_type,
                "rec_id": rec_id
            }
        )

    def create(self, vals):
        _logger.info("================================")
        fields = list(self._fields.keys())
        prev_record = self.read(fields)
        _logger.info(prev_record)
        record = super().create(vals)
        _logger.info(record)
        watched_fields = self._is_model_and_field_being_watched(
            model = self._name, 
            fields = self._fields.keys()
        )
        _logger.info(watched_fields)
        _logger.info(self._name)
        _logger.info(self._rec_name)
        if watched_fields["is_watched"]:
            for field in watched_fields["fields"]:
                _logger.info(field)
                _logger.info(field.field.name)
                if field.check_when_create:
                    for rec in record:
                        record_val = rec.read()[0]
                        _logger.info(record_val)
                        self._write_log(
                            model = field.model.id,
                            field = field.field.id,
                            record = record_val[self.name if not self._rec_name else self._rec_name],
                            prev_val = False,
                            next_val = record_val[field.field.name],
                            operation_type = "created",
                            rec_id = record_val["id"]
                        )
        
        _logger.info("================================")
        return record

    def write(self, vals):
        _logger.info("================================")
        fields = list(self._fields.keys())
        prev_record = self.read(fields)
        _logger.info(prev_record)
        _logger.info(vals)
        record = super().write(vals)
        _logger.info(record)
        watched_fields = self._is_model_and_field_being_watched(
            model = self._name, 
            fields = self._fields.keys()
        )
        _logger.info(watched_fields)
        _logger.info(self._name)
        _logger.info(self._rec_name)
        if watched_fields["is_watched"]:
            for field in watched_fields["fields"]:
                _logger.info(field)
                _logger.info(field.field.name)
                if field.check_when_update and field.field.name in list(vals.keys()):
                    _logger.info("......................................")
                    _logger.info(record)
                    _logger.info(field.field.name)
                    
                    _logger.info("......................................")
                    for index, rec in enumerate(prev_record):
                        record_val = self.read()
                        _logger.info(record_val)
                        self._write_log(
                            model = field.model.id,
                            field = field.field.id,
                            record = record_val[index][self.name if not self._rec_name else self._rec_name],
                            prev_val = prev_record[index][field.field.name],
                            next_val = record_val[index][field.field.name],
                            operation_type = "updated",
                            rec_id = self.id
                        )
        
        _logger.info("================================")
        return record

