from typing import List

from pydantic import BaseModel

from dentalink.schemas.api import DentalinkDataCursor


class DentalinkSucursalResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    ciudad: str
    comuna: str
    direccion: str
    habilitada: bool
    links: List[DentalinkDataCursor]
