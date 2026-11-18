"""
05_inventario_csv.py - Script propio del TP N° 4 (Redes de Computadoras 3643, Grupo 10)

Qué hace
--------
Arma un inventario completo de la red a partir de la API del Network Controller y lo
exporta a CSV. A diferencia de los scripts suministrados (que solo imprimen el JSON o una
tabla de un único endpoint), este script:
  1. Pide el ticket (POST /ticket) con el usuario del controlador.
  2. Consulta los equipos (GET /network-device) y los hosts (GET /host).
  3. Cruza cada host con el equipo al que está conectado.
  4. Marca los equipos que NO están en estado Managed (por ejemplo el ISP, que queda en
     "Wrong credential" a propósito).
  5. Guarda inventario_equipos.csv e inventario_hosts.csv y muestra un resumen por consola.

Uso
---
    set NC_PASS=<clave del controlador>        (Windows, cmd)
    python src/05_inventario_csv.py

Variables de entorno opcionales: NC_BASE_URL (por defecto http://localhost:58000/api/v1),
NC_USER (por defecto admin) y NC_PASS. Si NC_PASS no está definida, el script pide la clave
por teclado, así no queda escrita en el repositorio público.
"""
import csv
import os
import sys
from collections import Counter
from datetime import datetime
from getpass import getpass

import requests
from tabulate import tabulate

BASE_URL = os.environ.get("NC_BASE_URL", "http://localhost:58000/api/v1")
USERNAME = os.environ.get("NC_USER", "admin")
TIMEOUT = 10  # segundos


def obtener_ticket(password):
    """POST /ticket -> devuelve el serviceTicket que va en el header X-Auth-Token."""
    resp = requests.post(
        f"{BASE_URL}/ticket",
        json={"username": USERNAME, "password": password},
        headers={"Content-Type": "application/json"},
        timeout=TIMEOUT,
    )
    print(f"POST /ticket -> {resp.status_code}")
    resp.raise_for_status()
    return resp.json()["response"]["serviceTicket"]


def consultar(ruta, ticket):
    """GET a un endpoint con el ticket; devuelve la lista 'response' del JSON."""
    resp = requests.get(f"{BASE_URL}/{ruta}", headers={"X-Auth-Token": ticket}, timeout=TIMEOUT)
    print(f"GET /{ruta} -> {resp.status_code}")
    resp.raise_for_status()
    return resp.json().get("response", [])


def unir(valor):
    """Algunos campos vienen como lista (vecinos, interfaces): se pasan a texto."""
    if isinstance(valor, list):
        return " | ".join(str(v) for v in valor if v != "")
    return valor if valor not in (None, "") else "N/D"


def main():
    password = os.environ.get("NC_PASS") or getpass(f"Clave de {USERNAME} en el controlador: ")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        ticket = obtener_ticket(password)
        equipos = consultar("network-device", ticket)
        hosts = consultar("host", ticket)
    except requests.exceptions.ConnectionError:
        sys.exit("No se pudo conectar: ¿Packet Tracer está abierto y con el acceso externo habilitado?")
    except requests.exceptions.HTTPError as err:
        sys.exit(f"La API respondió con error: {err}")

    # --- Equipos -----------------------------------------------------------------------
    # Se usa get() porque los equipos inalcanzables no traen todas las claves (KeyError).
    filas_equipos = []
    for e in equipos:
        filas_equipos.append({
            "hostname": unir(e.get("hostname")),
            "tipo": unir(e.get("type")),
            "modelo": unir(e.get("platformId")),
            "ip_gestion": unir(e.get("managementIpAddress")),
            "estado_coleccion": unir(e.get("collectionStatus")),
            "alcanzabilidad": unir(e.get("reachabilityStatus")),
            "version_software": unir(e.get("softwareVersion")),
            "numero_serie": unir(e.get("serialNumber")),
            "vecinos": unir(e.get("connectedNetworkDeviceName")),
            "fecha_consulta": fecha,
        })

    # --- Hosts, cruzados con el equipo de acceso al que se conectan --------------------
    filas_hosts = []
    for h in hosts:
        filas_hosts.append({
            "host": unir(h.get("hostName")),
            "tipo": unir(h.get("hostType")),
            "ip": unir(h.get("hostIp")),
            "mac": unir(h.get("hostMac")),
            "equipo_conectado": unir(h.get("connectedNetworkDeviceName")),
            "ip_equipo_conectado": unir(h.get("connectedNetworkDeviceIpAddress")),
            "interfaz": unir(h.get("connectedInterfaceName")),
            "ping": unir(h.get("pingStatus")),
            "fecha_consulta": fecha,
        })

    # --- Exportar a CSV ----------------------------------------------------------------
    for nombre, filas in (("inventario_equipos.csv", filas_equipos), ("inventario_hosts.csv", filas_hosts)):
        if not filas:
            print(f"Sin datos para {nombre}, no se genera.")
            continue
        with open(nombre, "w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            escritor.writeheader()
            escritor.writerows(filas)
        print(f"Archivo generado: {nombre} ({len(filas)} filas)")

    # --- Resumen por consola -----------------------------------------------------------
    print("\n=== EQUIPOS ===")
    print(tabulate([[f["hostname"], f["tipo"], f["ip_gestion"], f["estado_coleccion"]] for f in filas_equipos],
                   headers=["Hostname", "Tipo", "IP de gestión", "Estado"], tablefmt="grid"))
    print("\n=== HOSTS ===")
    print(tabulate([[f["host"], f["ip"], f["equipo_conectado"], f["interfaz"], f["ping"]] for f in filas_hosts],
                   headers=["Host", "IP", "Conectado a", "Interfaz", "Ping"], tablefmt="grid"))

    por_estado = Counter(f["estado_coleccion"] for f in filas_equipos)
    print("\nEquipos por estado:", dict(por_estado))
    fuera = [f["hostname"] if f["hostname"] != "N/D" else f["ip_gestion"]
             for f in filas_equipos if f["estado_coleccion"] != "Managed"]
    if fuera:
        print("ATENCIÓN - equipos que no están Managed:", ", ".join(fuera))
    else:
        print("Todos los equipos están en estado Managed.")


if __name__ == "__main__":
    main()
