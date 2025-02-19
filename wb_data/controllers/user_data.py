from odoo import http
from odoo.http import request
from datetime import datetime
import logging
import pytz


_logger = logging.getLogger(__name__)

class DashboardData(http.Controller):
    @http.route('/wb_data/get_user_info', type='json', auth='user')
    def user_data_get(self):

        user = request.env.user
        user_timezone = user.tz

        if user_timezone:
            local_tz = pytz.timezone(user_timezone)
            utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
            local_now = utc_now.astimezone(local_tz)   
            offset_minutes = local_now.utcoffset().total_seconds() / 60
            offset_hours = int(offset_minutes // 60)  
            return { "utc_diff": offset_hours }    

        else:
            return { "utc_diff": 0 }    
