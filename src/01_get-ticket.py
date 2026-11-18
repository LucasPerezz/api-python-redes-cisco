import json
import os
import getpass
import requests
BASE_URL = os.environ.get("NC_BASE_URL", "http://localhost:58000/api/v1")
api_url = BASE_URL + "/ticket"

headers = {
    "content-type": "application/json"
}

body_json = {
    "username": os.environ.get("NC_USER", "admin"),
    "password": os.environ.get("NC_PASS") or getpass.getpass("Clave del controlador: ")
}

resp = requests.post(api_url, json.dumps(body_json), headers=headers)

print("Ticket request status: ", resp.status_code)
response_json = resp.json()
print (response_json)
serviceTicket = response_json["response"]["serviceTicket"]

print("The service ticket number is: ", serviceTicket) 
