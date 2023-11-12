from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, field_validator

from dentalink.schemas.api import DentalinkDataCursor


class DentalinkCitaResponse(BaseModel):
    id: int
    id_paciente: int
    nombre_paciente: str
    nombre_social_paciente: str
    id_estado: int
    estado_cita: str
    estado_anulacion: int
    estado_confirmacion: int
    id_tratamiento: int
    nombre_tratamiento: str
    tratamiento_sin_asignar: int
    fecha: datetime
    hora_inicio: str
    hora_fin: str
    duracion: int
    id_dentista: int
    nombre_dentista: str
    id_sucursal: int
    nombre_sucursal: str
    motivo_atencion: Union[str, None] = None
    id_sillon: int
    nombre_sillon: str
    id_lugar_atencion: Union[int, None] = None
    nombre_lugar_atencion: Union[str, None] = None
    comentarios: str
    fecha_actualizacion: datetime
    links: List[DentalinkDataCursor]

    @field_validator("fecha", mode="before")
    @classmethod
    def parse_date_format(cls, v: str) -> datetime:
        return datetime.strptime(v, "%Y-%m-%d")

    @field_validator("fecha_actualizacion", mode="before")
    @classmethod
    def parse_datetime_format(cls, v: str) -> datetime:
        return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")


class DentalinkEstadoCitaResponse(BaseModel):
    id: int
    nombre: str
    color: str
    reservado: bool
    anulacion: bool
    uso_interno: bool
    habilitado: bool
    links: List[DentalinkDataCursor]
