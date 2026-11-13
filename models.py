from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Ocorrencia(Base):
    __tablename__ = "ocorrencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    rodovia: Mapped[str] = mapped_column(String(10), index=True)
    tipo: Mapped[str] = mapped_column(String(20))
    km: Mapped[int]
    descricao: Mapped[str | None] = mapped_column(String(200))