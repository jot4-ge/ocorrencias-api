from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TipoOcorrencia = Literal["acidente", "buraco", "alagamento", "obstrucao"]


class OcorrenciaCreate(BaseModel):
    rodovia: str = Field(pattern=r"^BR-\d{3}$")
    tipo: TipoOcorrencia
    km: int = Field(ge=0, le=5000)
    descricao: str | None = Field(default=None, max_length=200)


class OcorrenciaUpdate(BaseModel):
    rodovia: str | None = Field(default=None, pattern=r"^BR-\d{3}$")
    tipo: TipoOcorrencia | None = None
    km: int | None = Field(default=None, ge=0, le=5000)
    descricao: str | None = Field(default=None, max_length=200)


class OcorrenciaResponse(OcorrenciaCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int