from fastapi import FastAPI, HTTPException, Query 
from schemas import OcorrenciaCreate, OcorrenciaResponse, OcorrenciaUpdate

app = FastAPI(title="API de Ocorrências")

# "Banco" em memória, só por hoje
ocorrencias = [
    {"id": 1, "rodovia": "BR-040", "tipo": "acidente", "km": 12},
    {"id": 2, "rodovia": "BR-060", "tipo": "buraco", "km": 87},
    {"id": 3, "rodovia": "BR-040", "tipo": "alagamento", "km": 45},
]


@app.get("/ocorrencias", response_model=list[OcorrenciaResponse])
def listar(
    rodovia: str | None = None,
    tipo: str | None = None,
    limite: int = Query(default=10, ge=1, le=50),
):
    resultado = ocorrencias
    if rodovia:
        resultado = [o for o in resultado if o["rodovia"] == rodovia]
    if tipo:
        resultado = [o for o in resultado if o["tipo"] == tipo]
    return resultado[:limite]

@app.get("/ocorrencias/total")
def total():
    return {"total": len(ocorrencias)}

@app.get("/ocorrencias/{ocorrencia_id}", response_model=OcorrenciaResponse)
def buscar(ocorrencia_id: int):  
    for o in ocorrencias:
        if o["id"] == ocorrencia_id:
            return o
    raise HTTPException(status_code=404, detail="Ocorrência não encontrada")


@app.delete("/ocorrencias/{ocorrencia_id}", status_code=204)
def deletar(ocorrencia_id: int):
    for i, o in enumerate(ocorrencias):
        if o["id"] == ocorrencia_id:
            ocorrencias.pop(i)
            return
    raise HTTPException(status_code=404, detail="Ocorrência não encontrada")

@app.post("/ocorrencias", response_model=OcorrenciaResponse, status_code=201)
def criar(dados: OcorrenciaCreate):
    novo_id = max((o["id"] for o in ocorrencias), default=0) + 1
    nova = {"id": novo_id, **dados.model_dump()}
    ocorrencias.append(nova)
    return nova


@app.patch("/ocorrencias/{ocorrencia_id}", response_model=OcorrenciaResponse)
def atualizar_parcial(ocorrencia_id: int, dados: OcorrenciaUpdate):
    for o in ocorrencias:
        if o["id"] == ocorrencia_id:
            o.update(dados.model_dump(exclude_unset=True))
            return o
    raise HTTPException(status_code=404, detail="Ocorrência não encontrada")