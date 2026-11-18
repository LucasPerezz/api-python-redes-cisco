import json
import os
import getpass
import requests

BASE_URL = os.environ.get("NC_BASE_URL", "http://localhost:58000/api/v1")

def obtener_ticket():
    """Pide un ticket nuevo (cambia en cada sesion y vence)."""
    body = {"username": os.environ.get("NC_USER", "admin"),
            "password": os.environ.get("NC_PASS") or getpass.getpass("Clave del controlador: ")}
    r = requests.post(BASE_URL + "/ticket", json.dumps(body), headers={"content-type": "application/json"})
    return r.json()["response"]["serviceTicket"]

api_url = BASE_URL + "/network-device"

headers = {"X-Auth-Token": obtener_ticket()}

resp = requests.get(api_url, headers=headers)

print("Request status: ", resp.status_code)

response_json = resp.json()
print()
print()
print (response_json)
print()
print()
networkDevices = response_json["response"]

for networkDevice in networkDevices:
    print(networkDevice.get("hostname") or "N/D", "\t", networkDevice.get("platformId") or "N/D", "\t", networkDevice.get("managementIpAddress") or "N/D")
