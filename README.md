# Dentalink Client
Librería de Python para interactuar con la API de [dentalink](https://api.dentalink.healthatom.com/docs).

_Realizado en el contexto de prueba técnica para [cero.ai](https://www.cero.ai/)_
# Supuestos

Dado el contexto de la empresa, que busca integrar su solucion en distintos softwares, y dado los requerimientos de la prueba técnica, se tomaron los siguientes supuestos:

- **Librería de Python**: Se asumió que éste cliente sería usado en el contexto de la programación de una integración (es decir, se programaría en python algo que requería de poder conectarse con la API de Dentalink), es por esto que se optó por crear una librería en vez de, por ejemplo, un CLI.
- **Python 3.9+**: Se asumió que se usaría python 3.9 en adelante.
- **Código sincrónico**: Si se programaba esta librería usando asincronía (`aiohttp` o `httpx`) sería muy complicado su uso en contextos donde el programa esté basado en código sincrónico, forzando a escribir dos tipos de cliente. Se asume entonces que el contexto es sincrónico.

# Descripción de la solución
Cliente escrito en python que mediante la librería `requests` realiza peticiones a la API de [dentalink](https://api.dentalink.healthatom.com/docs).

## Características
- Las consultas retornan un objeto de `pydantic` que permite una interacción sencilla con las respuestas de la API
- Se reutiliza la sesión en cada petición.
- Están implementadas:
    - Obtención de todas las citas con filtros.
    - Obtención de una cita según id de la cita.
    - Modificación de una cita según id de la cita.
    - Obtención de todas las sucursales con filtros.
    - Obtención de todos los estados de cita con filtros.

# Ejemplos de uso

**Inicialización**
```py
from dentalink.client import DentalinkClient

url = "https://api.dentalink.healthatom.com/api/v1"
token = "MY_SUPER_SECRET_TOKEN"
client = DentalinkClient(url, token=token)

# Tambien se puede omitir la url, y utilizará /api/v1 por defecto
client = DentalinkClient(token=token)
```

**Obtención de citas**
```py
response = client.obtener_citas()

>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkCitaResponse(...)
    ]
)
"""

# Podemos usar los filtros también (son opcionales)
response = client.obtener_citas(
    start_date=datetime(2023, 11, 13),
    end_date=datetime(2023, 11, 15),
    id_estado=7,
    id_sucursal=1,
)

>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkCitaResponse(...)
    ]
)
"""

# Y podemos obtener una única cita
response = client.obtener_cita_segun_id(id_cita=1)
>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkCitaResponse(...)
    ]
)
"""
```
_Más información en https://github.com/Keviinplz/dentalink/blob/main/dentalink/client.py#L105_

**Modificación del estado de una cita**
```py
id_cita = 305

response = client.actualizar_cita_segun_id(id_cita, id_estado=2)
>>> print(response)
"""
DentalinkResponse(
    links=None,
    data=DentalinkCitaResponse(...)
)
"""
```

**Obtención de sucursales**
```py
# Obtiene todas las sucursales
response = client.obtener_sucursales()
>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkSucursalResponse(...)
    ]
)
"""

# Podemos usar los filtros definidos en la API
response = client.obtener_sucursales(nombre="foo")
>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkSucursalResponse(...)
    ]
)
"""
```

**Obtención de estados de cita**
```py
# Obtiene todos los estados de cita
response = client.obtener_estados_de_cita()
>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkEstadoCitaResponse(...)
    ]
)
"""

# Podemos usar los filtros definidos en la API
response = client.obtener_estados_de_cita(nombre="foo")
>>> print(response)
"""
DentalinkResponse(
    links=DentalinkCursor(
        current="...",
        next="...",
        prev="..."
    ),
    data=[
        ...,
        DentalinkSucursalResponse(...)
    ]
)
"""
```