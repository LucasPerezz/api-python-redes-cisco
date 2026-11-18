# API Python - Redes de Computadoras (3643) - TP N° 4 - Grupo 10

Scripts de Python que consumen la API REST del Network Controller de Cisco Packet Tracer
(`http://localhost:58000/api/v1`). Partimos de los scripts de la cátedra
(`redes-computadoras/api-python-redes-cisco`), les sacamos las credenciales y el ticket escritos en el código, y agregamos un script propio.

## Scripts

| Script | Qué hace | Endpoints |
|---|---|---|
| `src/01_get-ticket.py` | Obtiene el ticket de sesión (`serviceTicket`) con el usuario del controlador. | `POST /ticket` |
| `src/02_get-network-device.py` | Lista los equipos del inventario del controlador. Pide su ticket. | `GET /network-device` |
| `src/03_get-host.py` | Lista los hosts que ve el controlador (nombre, IP, MAC, equipo e interfaz de conexión). | `GET /host` |
| `src/04_tabulate.py` | Muestra los equipos en una tabla (número, hostname, serie, versión). | `POST /ticket`, `GET /network-device` |
| `src/05_inventario_csv.py` | **Script propio.** Une equipos y hosts, marca los equipos que no están en estado Managed y exporta `inventario_equipos.csv` e `inventario_hosts.csv`. | `POST /ticket`, `GET /network-device`, `GET /host` |

## Instalación (Windows)

```
git clone <URL de este repositorio>
cd <carpeta>
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

El entorno virtual (`.venv`) y los archivos con claves no se suben al repositorio.

## Uso

1. Abrir el `.pkt` en Packet Tracer con el controlador funcionando y el acceso externo habilitado.
2. Definir el usuario y la clave del controlador (si no se define la clave, el script la pide por teclado):
   `set NC_USER=admin` y `set NC_PASS=<clave>`.
3. Los cinco scripts piden su propio ticket, no hay que copiarlo a mano.

```
set NC_PASS=<clave del controlador>
python src/05_inventario_csv.py
```

Variables opcionales: `NC_BASE_URL` (por defecto `http://localhost:58000/api/v1`) y `NC_USER`
(por defecto `admin`), válidas para todos los scripts.

## Salida del script propio

- `inventario_equipos.csv`: hostname, tipo, modelo, IP de gestión, estado de colección, versión,
  número de serie y vecinos de cada equipo.
- `inventario_hosts.csv`: host, tipo, IP, MAC, equipo e interfaz de conexión y estado del ping.
- En consola: tablas de equipos y hosts, cantidad de equipos por estado y aviso de los que no
  están en estado Managed (el ISP queda en *Wrong credential* a propósito: es el límite del
  sistema autónomo).

## Integrantes

PEREZ, Lucas Tomás - ALTAMIRANO, Franco - DOMINGUEZ, Fabricio. Comisión 02-3900.
