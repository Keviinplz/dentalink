import json
import urllib.parse
from datetime import datetime
from typing import Any, Union

import requests

from dentalink.exceptions import (
    DentalinkClientHTTPException,
)
from dentalink.query import DentalinkQuery
from dentalink.schemas.api import DentalinkResponse
from dentalink.schemas.citas import DentalinkCitaResponse, DentalinkEstadoCitaResponse
from dentalink.schemas.sucursales import DentalinkSucursalResponse


class DentalinkClient:
    """
    Cliente de la API de Dentalink
    https://api.dentalink.healthatom.com/docs

    Parámetros:
        url: String que representa la URL de conexión a la API (Por defecto: https://api.dentalink.healthatom.com/api/v1)
        token: String que representa el token de autorización (Ver: https://api.dentalink.healthatom.com/docs/#autenticacin)
    """

    def __init__(
        self, url: str = "https://api.dentalink.healthatom.com/api/v1", *, token: str
    ):
        session = requests.session()
        session.headers.update({"Authorization": f"Token {token}"})
        self._session = session
        self._url = url

    def __make_uri(
        self, endpoint: str, query: Union[dict[str, Any], None] = None
    ) -> str:
        """Retorna la uri final para la API

        Se encarga de juntar la URL base de la API con el endpoint proporcionado.
        A su vez realiza un encode usando 'urllib.parse.quote' de la query proporcionada
        retornando la URI completa

        Parámetros:
            endpoint: Recurso a solicitar
            query: Parámetro opcional que contiene los filtros a realizar en la petición (Ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Un string que representa la URI completa a donde solicitar la información
        """
        if not query or len(query) == 0:
            return self._url + endpoint

        # Al especificar `safe`, el método `quote` se comporta igual que `encodeURI` de Javascript
        # Que es lo usado en los ejemplos de la documentación de la API
        # Ver https://api.dentalink.healthatom.com/docs/ donde en los ejemplos se usa `encodeURI`
        # Y revisar https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/encodeURI#descripci%C3%B3n
        # Donde se especifica los carácteres omitidos.
        encoded = urllib.parse.quote(json.dumps(query), safe="@#$&()*!+=:;,?/'")

        return self._url + endpoint + "?q=" + encoded

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        query: Union[DentalinkQuery, None] = None,
        data: Union[dict[str, Union[str, int]], None] = None,
    ) -> dict[str, Any]:
        """Realiza una petición a la API

        El método construye la URI a usar y envía la petición a la API
        Se encarga de gestionar la respuesta y retorna los datos en formato JSON

        Parámetros:
            method: Método HTTP a utilizar (GET, POST, PUT, DELETE, etc...)
            endpoint: Recurso a solicitar
            query: Parámetro opcional que contiene los filtros a realizar en la petición (Ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)
            data: Parámetro opcional que contiene los datos a enviar (se envían en formato JSON vía body de la petición)

        Retorna:
            Un diccionario con la respuesta de la petición

        Errores:
            dentalink.exceptions.DentalinkClientHTTPException: La respuesta de la API no fue satistactoria (el código no es 200)
        """
        uri = self.__make_uri(endpoint, query=query.parse() if query else None)
        response = self._session.request(method, uri, json=data)

        if response.status_code != 200:
            try:
                parsed = response.json()
            except requests.exceptions.JSONDecodeError:
                raise DentalinkClientHTTPException(
                    code=response.status_code,
                    message=f"Error inesperado: {response.text}",
                )
            raise DentalinkClientHTTPException(
                code=response.status_code, message=parsed["error"]["message"]
            )

        return response.json()

    def obtener_citas(
        self,
        *,
        start_date: Union[datetime, None] = None,
        end_date: Union[datetime, None] = None,
        id_sucursal: Union[int, None] = None,
        id_estado: Union[int, None] = None,
    ):
        """Obtiene el listado de todas las citas de la clínica (ver: https://api.dentalink.healthatom.com/docs/#get-citas)

        Parámetros:
            start_date: Parámetro opcional que permite definir una fecha (datetime) como límite inferior (inclusivo).
            end_date: Parámetro opcional que permite definir una fecha (datetime) como límiter superior (inclusivo).
            id_surcursal: Entero positivo que representa la ID de una surcursal (ver: https://api.dentalink.healthatom.com/docs/#sucursales).
            id_estado: Entero positivo que representa la ID de un estado de cita (ver: https://api.dentalink.healthatom.com/docs/#estados-de-cita).

        Retorna:
            Objeto `DentalinkResponse` con el resultado de la petición, donde el atributo `data` es
            una lista de objetos `DentalinkCitaResponse`

        Errores:
            `dentalink.exceptions.DentalinkClientHTTPException`: La respuesta de la API no fue satistactoria (el código no es 200)
        """
        endpoint = "/citas"

        q = (
            DentalinkQuery("fecha")
            .gte(start_date)
            .lte(end_date)
            .field("id_sucursal")
            .eq(id_sucursal)
            .field("id_estado")
            .eq(id_estado)
        )

        response = self._request("GET", endpoint, query=q)

        return DentalinkResponse(
            links=response.get("links"),
            data=[DentalinkCitaResponse(**data) for data in response["data"]],
        )

    def obtener_estados_de_cita(
        self,
        *,
        nombre: Union[str, None] = None,
        reservado: Union[bool, None] = None,
        anulacion: Union[bool, None] = None,
        uso_interno: Union[bool, None] = None,
        habilitado: Union[bool, None] = None,
    ):
        """Obtiene el listado de todos los estados de cita disponibles (ver: https://api.dentalink.healthatom.com/docs/#get-citasestados)

        Parámetros:
            nombre: String opcional que permite filtrar por nombre del estado de cita.
            reservado: Boolean opcional que permite filtrar por estado de reservación.
            anulacion: Boolean opcional que permite filtrar por estado de anulación.
            uso_interno: Boolean opcional que permite filtrar por estado de uso interno.
            habilitado: Boolean opcional que permite filtrar estados habilitados o no.

        Retorna:
            Objeto `DentalinkResponse` con el resultado de la petición, donde el atributo `data` es
            una lista de objetos `DentalinkEstadoCitaResponse`

        Errores:
            `dentalink.exceptions.DentalinkClientHTTPException`: La respuesta de la API no fue satistactoria (el código no es 200)
        """
        endpoint = "/citas/estados"
        q = (
            DentalinkQuery("nombre")
            .eq(nombre)
            .field("reservado")
            .eq(reservado)
            .field("anulacion")
            .eq(anulacion)
            .field("uso_interno")
            .eq(uso_interno)
            .field("habilitado")
            .eq(habilitado)
        )

        response = self._request("GET", endpoint, query=q)

        return DentalinkResponse(
            links=response.get("links"),
            data=[DentalinkEstadoCitaResponse(**data) for data in response["data"]],
        )

    def obtener_sucursales(
        self, *, nombre: Union[str, None] = None, habilitada: Union[bool, None] = None
    ):
        """Obtiene el listado de todas las sucursales de la clínica (ver: https://api.dentalink.healthatom.com/docs/#get-sucursales)

        Parámetros:
            nombre: String opcional que permite filtrar por nombre de la sucursal.
            habilitado: Boolean opcional que permite filtrar sucursales habilitadas o inhabilitadas.

        Retorna:
            Objeto `DentalinkResponse` con el resultado de la petición, donde el atributo `data` es
            una lista de objetos `DentalinkSucursalResponse`

        Errores:
            `dentalink.exceptions.DentalinkClientHTTPException`: La respuesta de la API no fue satistactoria (el código no es 200)
        """

        endpoint = "/sucursales"
        q = DentalinkQuery("nombre").eq(nombre).field("habilitada").eq(habilitada)

        response = self._request("GET", endpoint, query=q)

        return DentalinkResponse(
            links=response.get("links"),
            data=[DentalinkSucursalResponse(**data) for data in response["data"]],
        )

    def obtener_cita_segun_id(self, id_cita: int):
        """Obtiene una única cita según la ID de la cita (ver: https://api.dentalink.healthatom.com/docs/#get-citasid_cita)

        Parámetros:
            id_cita: Entero positivo que representa la ID de la cita a buscar.

        Retorna:
            Objeto `DentalinkResponse` con el resultado de la petición, donde el atributo `data` es
            un objeto `DentalinkEstadoCitaResponse`

        Errores:
            `dentalink.exceptions.DentalinkClientHTTPException`: La respuesta de la API no fue satistactoria (el código no es 200)
        """
        endpoint = f"/citas/{id_cita}"

        response = self._request("GET", endpoint)

        return DentalinkResponse(
            links=response.get("links"),
            data=DentalinkCitaResponse(**response["data"]),
        )

    def actualizar_cita_segun_id(
        self,
        id_cita: int,
        *,
        duracion: Union[int, None] = None,
        id_estado: Union[int, None] = None,
        comentarios: Union[str, None] = None,
        flag_notificar_anulacion: Union[bool, None] = None,
    ):
        """Actualiza la información de una cita según la ID de ésta (ver: https://api.dentalink.healthatom.com/docs/#put-citasid_cita)

        Parámetros:
            id_cita: Entero positivo que representa la ID de la cita a buscar.
            duracion: Entero positivo opcional que representa la duración en minutos
            id_estado: Entero positivo opcional que representa la ID de un estado de cita (ver: https://api.dentalink.healthatom.com/docs/#estados-de-cita).
            comentarios: String opcional que representa un comentario adjunto a la cita.
            flag_notificar_anulacion: Bool opcional que permite enviar un correo al paciente notificando la anulación.

        Retorna:
            Objeto `DentalinkResponse` con el resultado de la petición, donde el atributo `data` es
            un objeto `DentalinkCitaResponse`

        Errores:
            `dentalink.exceptions.DentalinkClientHTTPException`: La respuesta de la API no fue satistactoria (el código no es 200)
        """
        endpoint = f"/citas/{id_cita}"
        data: dict[str, Union[int, str, bool]] = {}

        if duracion:
            data["duracion"] = duracion

        if id_estado:
            data["id_estado"] = id_estado

        if comentarios:
            data["comentarios"] = comentarios

        if flag_notificar_anulacion:
            data["flag_notificar_anulacion"] = True

        response = self._request("PUT", endpoint, data=data)

        return DentalinkResponse(
            links=response.get("links"),
            data=DentalinkCitaResponse(**response["data"]),
        )


__all__ = ["DentalinkClient"]
