from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import OcorrenciaCreate, OcorrenciaResponse, OcorrenciaUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Ocorrências")


def buscar_ou_404(db: Session, ocorrencia_id: int) -> models.Ocorrencia:
    obj = db.get(models.Ocorrencia, ocorrencia_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
    return obj


@app.get("/ocorrencias", response_model=list[OcorrenciaResponse])
def listar(
    rodovia: str | None = None,
    tipo: str | None = None,
    limite: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    stmt = select(models.Ocorrencia)
    if rodovia:
        stmt = stmt.where(models.Ocorrencia.rodovia == rodovia)
    if tipo:
        stmt = stmt.where(models.Ocorrencia.tipo == tipo)
    stmt = stmt.order_by(models.Ocorrencia.id).limit(limite)
    return db.scalars(stmt).all()


@app.get("/ocorrencias/total")
def total(db: Session = Depends(get_db)):
    return {"total": db.scalar(select(func.count()).select_from(models.Ocorrencia))}


@app.get("/ocorrencias/{ocorrencia_id}", response_model=OcorrenciaResponse)
def buscar(ocorrencia_id: int, db: Session = Depends(get_db)):
    return buscar_ou_404(db, ocorrencia_id)


@app.post("/ocorrencias", response_model=OcorrenciaResponse, status_code=201)
def criar(dados: OcorrenciaCreate, db: Session = Depends(get_db)):
    obj = models.Ocorrencia(**dados.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.put("/ocorrencias/{ocorrencia_id}", response_model=OcorrenciaResponse)
def atualizar(ocorrencia_id: int, dados: OcorrenciaCreate, db: Session = Depends(get_db)):
    obj = buscar_ou_404(db, ocorrencia_id)
    for campo, valor in dados.model_dump().items():
        setattr(obj, campo, valor)
    db.commit()
    db.refresh(obj)
    return obj


@app.patch("/ocorrencias/{ocorrencia_id}", response_model=OcorrenciaResponse)
def atualizar_parcial(ocorrencia_id: int, dados: OcorrenciaUpdate, db: Session = Depends(get_db)):
    obj = buscar_ou_404(db, ocorrencia_id)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(obj, campo, valor)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/ocorrencias/{ocorrencia_id}", status_code=204)
def deletar(ocorrencia_id: int, db: Session = Depends(get_db)):
    obj = buscar_ou_404(db, ocorrencia_id)
    db.delete(obj)
    db.commit()