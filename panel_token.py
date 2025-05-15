import requests
import json

import config


url_panel = config.ahriman_url
username_panel = config.ahriman_user
password_panel = config.ahriman_pass

token_url = url_panel + "/api/admins/token"
data_token = {
    'username': username_panel,
    'password': password_panel
}

response = requests.post(token_url, data=data_token, headers={
    'Content-Type': 'application/x-www-form-urlencoded',
    'accept': 'application/json'
})

token_data = response.json()
access_token = token_data.get("access_token")

if not access_token:
    print("Error getting token:", token_data)
else:
    services_url = url_panel + "/api/services"
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Accept': 'application/json'
    }

    response = requests.get(services_url, headers=headers)
    services = response.json()

    if "items" in services:
        print("لیست سرویس‌ها:")
        for s in services["items"]:
            print(f"Name: {s['name']}, ID: {s['id']}")
    else:
        print("پاسخ نامعتبر یا خطا در دریافت سرویس‌ها:", services)
