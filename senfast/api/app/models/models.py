# Modelos
from pydantic import BaseModel
from typing import Literal


class BarriRead(BaseModel):
    CODI_BARRI: int
    NOM_BARRI: str
    # BAIXA: Literal['S', 'N']
