from odoo import models, fields, api
from datetime import datetime
import logging
import threading
import time
import traceback

_logger = logging.getLogger(__name__)

THREAD_LIMIT = 10  # Adjust based on server capacity
thread_semaphore = threading.Semaphore(THREAD_LIMIT)

class WriteInLog(models.BaseModel):
    _inherit = "base"

    def _safe_write_update_log(self, prev_record, vals, new_record):
        """Thread-safe ORM operation with explicit cursor closing."""
        with thread_semaphore:  # Limit concurrent threads
            try:
                with self.env.registry.cursor() as cr:
                    env = api.Environment(cr, self.env.uid, self.env.context)
                    start = time.perf_counter()
                    watched_fields = env["wb_log.watched_fields"].search(
                        [("model.model", "=", self._name), ("field.name", "in", list(vals.keys()))]
                    )
                    end = time.perf_counter()
                    _logger.info(f"Time elapsed for the search {end-start}")
                    if watched_fields:
                        for field in watched_fields:
                            if field.check_when_update:
                                for index, rec in enumerate(prev_record):
                                    env["wb_log.log"].create({
                                        "record": new_record[index][self._rec_name or "name"],
                                        "model": field.model.id,
                                        "field": field.field.id,
                                        "user": env.user.id,
                                        "at": datetime.now(),
                                        "prev_value": prev_record[index][field.field.name],
                                        "new_value": new_record[index][field.field.name],
                                        "movment_type": "updated",
                                        "rec_id": new_record[index]["id"]
                                    })
                    cr.commit()

            except Exception as e:
                _logger.error(f"Error in _write_update_log thread: {e}")

    def write(self, vals):
        _logger.info("WRITE METHOD")
        if self.env.registry.ready:
            try:
                _logger.info("ODOO INITIALIZED")
                  # Only use threads if Odoo is fully initialized
                """Override write method to use threading only when Odoo is fully loaded."""
                _logger.info("------------------------------------")
                _logger.info(self._fields.keys())
                prev_record = self.read(list(self._fields.keys()))
                _logger.info("prev record read")
                result = super().write(vals)
                new_record = self.read(list(self._fields.keys()))
                _logger.info(prev_record)
                _logger.info(result)
                _logger.info(new_record)
                _logger.info("------------------------------------")

                _logger.info("THREAD INITIALIZED")

                thread = threading.Thread(
                    target=self._safe_write_update_log,
                    args=(prev_record, vals, new_record),
                    daemon=True
                )
                thread.start()
            except Exception as e:  
                _logger.error("******************ERROR ON READ*******************")
                _logger.error(traceback.format_exc())
                _logger.error(f"Error in write method: {e}")
                _logger.error("******************ERROR ON READ*******************")
        else:
            _logger.info("ODOO NOT INITIALIZED")
            result = super().write(vals)
        return result

    def _safe_write_delete_log(self, prev_record):
        """Thread-safe delete logging."""
        with thread_semaphore:  # Limit concurrent threads
            try:
                with self.env.registry.cursor() as cr:
                    env = api.Environment(cr, self.env.uid, self.env.context)

                    start = time.perf_counter()
                    watched_fields = env["wb_log.watched_fields"].search(
                        [("model.model", "=", self._name)]
                    )
                    end = time.perf_counter()
                    _logger.info(f"Time elapsed for the search {end-start}")
                    if watched_fields:
                        for field in watched_fields:
                            if field.check_when_remove:
                                for rec in prev_record:
                                    env["wb_log.log"].create({
                                        "record": rec[self._rec_name or "name"],
                                        "model": field.model.id,
                                        "field": field.field.id,
                                        "user": env.user.id,
                                        "at": datetime.now(),
                                        "prev_value": rec[field.field.name],
                                        "new_value": False,
                                        "movment_type": "deleted",
                                        "rec_id": rec["id"]
                                    })
                    cr.commit()

            except Exception as e:
                _logger.error(f"Error in _write_delete_log thread: {e}")

    def unlink(self):
        if self.env.registry.ready:  # Only use threads if Odoo is fully initialized
            """Override unlink method to use threading only when Odoo is fully loaded."""
            prev_record = self.read(list(self._fields.keys()))
            _logger.info("------------------------------------")
            _logger.info(self._fields.keys())
            _logger.info("------------------------------------")
            result = super().unlink()
            thread = threading.Thread(
                target=self._safe_write_delete_log,
                args=(prev_record,),
                daemon=True
            )
            thread.start()
        else:
            result = super().unlink()
        return result

