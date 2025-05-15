from api_panel import adduserm
from datetime import datetime, timedelta
import json

import config

panel_info = {
    "url_panel": config.ahriman_url,
    "username_panel": config.ahriman_user,    
    "password_panel": config.ahriman_pass,     
    "datelogin": None,
    "name_panel": "main",
    "proxies": json.dumps([config.ahriman_id_panel]),        
    "onholdstatus": "offonhold"           
}


def ahriman_add_user(ser_time, ser_data, ser_name):
    if not isinstance(ser_time, int) or not isinstance(ser_data, int) or not isinstance(ser_name, str):
        return {"status": "error", "message": "Invalid input types."}

    username = ser_name
    data_limit = int(ser_data) * 1024 * 1024 * 1024 
    expire_in_days = int(ser_time)
    timestamp = int((datetime.now() + timedelta(days=expire_in_days)).timestamp())
    
    response = adduserm(panel_info, data_limit, username, timestamp)
    
    return response


