from datetime import datetime
from typing import List, Union

from dentalink.exceptions import (
    DentalinkClientQueryError,
)


class DentalinkQueryFactory:
    """Construye filtros para la API de Dentalink (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

    La API define una mecánica de filtros para utilizar en las peticiones,
    dicho filtros constan de un diccionario de campos que contienen operaciones.
    Esta clase busca facilitar la creación de dicho filtros.

    Parámetros
        field: String que representa el campo inicial (opcional)

    Módo de uso
    ```py
        >>> (DentalinkQueryFactory().field('foo').eq(3)
            .field('bar').gt(1).lt(3)
            .field('now').eq(datetime(2023, 11, 12), dt_format='%Y-%m-%d')
            .parse())
        {
            "foo": { "eq": 3 },
            "bar": [{"gt": 1}, {"lt": 3}],
            "now": { "eq": "2023-11-12" }
        }
    ```
    """

    def __init__(self, field: Union[str, None] = None):
        self._query: dict[str, List[dict[str, str]]] = {}
        self._last_field: Union[str, None] = None

        if field:
            self._set_field(field)

    def _cast_value_to_str(
        self,
        value: Union[int, float, datetime, bool, str],
        dt_format: Union[str, None] = None,
    ) -> str:
        """Convierte el valor en un string

        Formatea el valor según el tipo, si es un datetime, lo convertirá a string según el formato dado,
        si es un booleano, lo convertirá en un string con la representación 0 o 1 (con 1 True), para el resto
        de tipos lo convertirá en string.

        Parámetros:
            value: Valor a castear, puede ser entero, flotante, datetime, booleano o string.
            dt_format: Parámetro opcional que representa el formato a considerar para castear un datetime.
            En caso de que value sea datetime y este parámetro no se encuentre, arrojará un error.

        Retorna:
            String que corresponde al valor casteado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de error con un campo no añadido o formato inválido.
        """
        if isinstance(value, datetime):
            if dt_format is None:
                raise DentalinkClientQueryError(
                    "Debes proporcionar un formato si el valor es un datetime"
                )
            return value.strftime(dt_format)

        if isinstance(value, bool):
            return "1" if value else "0"

        return str(value)

    def _set_field(self, field: str) -> None:
        """Agrega un nuevo campo a la query

        Parámetros
            field: Nuevo campo a agregar
        """
        self._last_field = field
        self._query[field] = []

    def _add_filter(
        self,
        name: str,
        value: Union[int, float, datetime, bool, str, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Agrega un nuevo filtro

        Parámetros:
            name: String que representa el nombre del operador (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores).
            value: Parámetro opcional que contiene el valor del operador.
            dt_format: Parámetro opcional que contiene el formato datetime a usar si es que el valor es un datetime.

        Retorna:
            Este mismo objeto, pero con el filtro añadido

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {name: self._cast_value_to_str(value, dt_format)}
        )
        return self

    def field(self, field_name: str) -> "DentalinkQueryFactory":
        """Agrega un nuevo campo

        Parámetros:
            field_name: String que representa el nombre del campo a agregar.

        Retorna:
            Este mismo objeto, pero con el campo agregado
        """
        if self._last_field == field_name:
            return self

        self._set_field(field_name)
        return self

    def eq(
        self,
        value: Union[int, float, datetime, bool, str, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `eq` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `eq` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("eq", value, dt_format)

    def neq(
        self,
        value: Union[int, float, datetime, bool, str, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `neq` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `neq` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("neq", value, dt_format)

    def gt(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `gt` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `gt` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("gt", value, dt_format)

    def gte(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `gte` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `gte` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("gte", value, dt_format)

    def lt(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `lt` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `lt` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("lt", value, dt_format)

    def lte(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `lte` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `lte` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("lte", value, dt_format)

    def lk(
        self, value: Union[datetime, None] = None, dt_format: str = "%Y-%m-%d"
    ) -> "DentalinkQueryFactory":
        """Implementación del operador `lk` (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Retorna:
            Este mismo objeto, pero con el filtro `lk` agregado

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente agregar un filtro cuando no se ha configurado un campo.
        """
        return self._add_filter("lk", value, dt_format)

    def parse(self) -> dict[str, Union[dict[str, str], List[dict[str, str]]]]:
        """Retorna los filtros en el formato que la API espera (ver: https://api.dentalink.healthatom.com/docs/#filtros-y-cursores)

        Omite los campos sin filtros

        Retorna:
            Diccionario con los filtros en el formato de la API

        Errores:
            `dentalink.exceptions.DentalinkClientQueryError`: Arrojado en caso de que se intente llamar a este método sin haber configurado algún campo
        """
        if len(self._query) == 0:
            raise DentalinkClientQueryError(
                "No se ha proporcionado ningún campo para crear la consulta"
            )

        return {
            key: value[0] if len(value) == 1 else value
            for key, value in self._query.items()
            if len(value) > 0
        }
