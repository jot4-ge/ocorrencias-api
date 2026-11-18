from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Ocorrencia(Base):
    __tablename__ = "ocorrencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    rodovia: Mapped[str] = mapped_column(String(10), index=True)
    tipo: Mapped[str] = mapped_column(String(20))
    km: Mapped[int]
    descricao: Mapped[str | None] = mapped_column(String(200))
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )