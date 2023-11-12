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
    def __init__(self, url: str, *, token: str):
        session = requests.session()
        session.headers.update({"Authorization": f"Token {token}"})
        self._session = session
        self._url = url

    def __make_uri(
        self, endpoint: str, query: Union[dict[str, Any], None] = None
    ) -> str:
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
        endpoint = "/sucursales"
        q = DentalinkQuery("nombre").eq(nombre).field("habilitada").eq(habilitada)

        response = self._request("GET", endpoint, query=q)

        return DentalinkResponse(
            links=response.get("links"),
            data=[DentalinkSucursalResponse(**data) for data in response["data"]],
        )

    def obtener_cita_segun_id(self, id_cita: int):
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
        endpoint = f"/citas/{id_cita}"
        data = {}

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
