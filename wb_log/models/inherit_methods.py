from odoo import model, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class WriteInLog(models.BaseModel):

    def _is_model_and_field_being_watched(self, 
                                          model = None, 
                                          fields = None,
                                          field = None):

        if fields:
            watched_field = self.env["wb_log.watched_fields"].search(
                [
                    ("model.name", "=", model),
                    ("field.name", "in", fields)
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
                "field": str(field),
                "user": self.env.user,
                "at": datetime.now(),
                "prev_value": str(prev_val),
                "new_value": str(next_val),
                "movment_type": operation_type,
                "rec_id": rec_id
            }
        )

    def create(self, vals):
        _logger.info("================================")
        prev_record = self.read()
        _logger.info(prev_record)
        prev_record = self.read()
        record = super().create(vals)
        _logger.info(record)
        watched_fields = self._is_model_and_field_being_watched(
            name = self._name, 
            fields = self._fields.keys()
        )
        _logger.info(watched_fields)
        _logger.info(self._name)
        _logger.info(self._rec_name)
        _logger.info(record.read())
        _logger.info(record.id)
        if watched_fields["is_watched"]:
            for field in watched_fields["fields"]:
                if field.check_when_create:
                    self._write_log(
                        model = self._name,
                        field = field,
                        record = self._rec_name,
                        prev_val = False,
                        next_val = record[field],
                        operation_type = "created",
                        rec_id = record.id
                    )

        
        _logger.info("================================")
        return record

