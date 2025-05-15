import requests
import time
import json
from datetime import datetime

def token_panelm(panel):
    if panel.get("datelogin"):
        try:
            date = json.loads(panel["datelogin"])
            if "time" in date:
                start_date = time.time() - datetime.strptime(date["time"], "%Y/%m/%d %H:%M:%S").timestamp()
                if start_date <= 600:
                    return date
        except Exception:
            pass

    url_get_token = panel["url_panel"] + "/api/admins/token"
    data_token = {
        'username': panel["username_panel"],
        'password': panel["password_panel"]
    }

    try:
        response = requests.post(url_get_token, data=data_token, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        }, timeout=6)
        body = response.json()

        if 'access_token' in body:
            panel["datelogin"] = json.dumps({
                "time": datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                "access_token": body["access_token"]
            })
        return body
    except requests.RequestException as e:
        return {"error": str(e)}

def adduserm(panel, data_limit, username_ac, timestamp):
    Check_token = token_panelm(panel)
    if "access_token" not in Check_token:
        return {"error": "No access token"}
    
    url = panel["url_panel"] + "/api/users"
    header_value = "Bearer " + Check_token["access_token"]

    data = {
        "service_ids": json.loads(panel["proxies"]),
        "data_limit": data_limit,
        "username": username_ac
    }

    if panel["onholdstatus"] == "offonhold":
        if timestamp == 0:
            data["expire_date"] = None
            data["expire_strategy"] = "never"
        else:
            data["expire_date"] = datetime.utcfromtimestamp(timestamp).isoformat() + "Z"
            data["expire_strategy"] = "fixed_date"
    else:
        if timestamp == 0:
            data["expire_date"] = None
            data["expire_strategy"] = "never"
        else:
            data["expire_date"] = None
            data["expire_strategy"] = "start_on_first_use"
            data["usage_duration"] = timestamp - int(time.time())

    headers = {
        'Accept': 'application/json',
        'Authorization': header_value,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
