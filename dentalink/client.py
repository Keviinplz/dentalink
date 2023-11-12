import json
import urllib.parse
from datetime import datetime
from typing import Any, Union

import requests

from dentalink.exceptions import (
    DentalinkClientHTTPException,
)
from dentalink.query import DentalinkQuery


class DentalinkClient:
    def __init__(self, url: str, *, token: str):
        session = requests.session()
        session.headers.update({"Authorization": f"Token {token}"})
        self._session = session
        self._url = url

    def _make_uri(
        self, endpoint: str, query: Union[dict[str, Any], None] = None
    ) -> str:
        if not query or len(query) == 0:
            return self._url + endpoint

        return (
            self._url
            + endpoint
            + "?q="
            + urllib.parse.quote(json.dumps(query), safe="@#$&()*!+=:;,?/'")
        )

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
            .parse()
        )

        uri = self._make_uri(endpoint, q)
        response = self._session.get(uri)

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

    def cambiar_estado_de_cita(self, id_cita: int, *, id_estado: int):
        endpoint = f"/citas/{id_cita}"
        uri = self._make_uri(endpoint)

        response = self._session.put(uri, json={"id_estado": id_estado})

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
