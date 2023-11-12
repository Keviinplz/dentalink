from datetime import datetime
from typing import List, Union

from dentalink.exceptions import (
    DentalinkClientQueryError,
)


class DentalinkQuery:
    def __init__(self, field: Union[str, None] = None):
        self._query: dict[str, List[dict[str, str]]] = {}
        self._last_field = None

        if field:
            self._set_field(field)

    def _cast_value_to_str(
        self, value: Union[int, float, datetime, bool, str], dt_format: str
    ) -> str:
        if isinstance(value, datetime):
            return value.strftime(dt_format)

        if isinstance(value, bool):
            return "1" if value else "0"

        return str(value)

    def _set_field(self, field: str) -> None:
        self._last_field = field
        self._query[field] = []

    def field(self, field_name: str) -> "DentalinkQuery":
        if self._last_field == field_name:
            return self

        self._set_field(field_name)
        return self

    def eq(
        self,
        value: Union[int, float, datetime, bool, str, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"eq": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def neq(
        self,
        value: Union[int, float, datetime, bool, str, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"neq": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def gt(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"gt": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def gte(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"gte": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def lt(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"lt": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def lte(
        self,
        value: Union[int, float, datetime, None] = None,
        dt_format: str = "%Y-%m-%d",
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"lte": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def lk(
        self, value: Union[datetime, None] = None, dt_format: str = "%Y-%m-%d"
    ) -> "DentalinkQuery":
        if self._last_field is None:
            raise DentalinkClientQueryError(
                message="Debes establecer un campo usando .field() antes de agregar un filtro"
            )

        if value is None:
            return self

        self._query[self._last_field].append(
            {"lk": self._cast_value_to_str(value, dt_format)}
        )
        return self

    def parse(self) -> dict[str, Union[dict[str, str], List[dict[str, str]]]]:
        if len(self._query) == 0:
            raise DentalinkClientQueryError(
                "No se ha proporcionado ningún campo para crear la consulta"
            )

        return {
            key: value[0] if len(value) == 1 else value
            for key, value in self._query.items()
            if len(value) > 0
        }
