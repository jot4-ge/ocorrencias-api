import pytest

DADOS = {"rodovia": "BR-040", "tipo": "acidente", "km": 12}


def test_criar_ocorrencia(client):
    resp = client.post("/ocorrencias", json=DADOS)
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["id"] == 1
    assert corpo["rodovia"] == "BR-040"
    assert corpo["descricao"] is None


def test_tipo_invalido_retorna_422(client):
    resp = client.post("/ocorrencias", json={**DADOS, "tipo": "raio"})
    assert resp.status_code == 422


def test_buscar_inexistente_retorna_404(client):
    assert client.get("/ocorrencias/999").status_code == 404


def test_listar_com_filtros(client):
    client.post("/ocorrencias", json=DADOS)
    client.post("/ocorrencias", json={**DADOS, "tipo": "buraco"})
    client.post("/ocorrencias", json={**DADOS, "rodovia": "BR-060"})

    resp = client.get("/ocorrencias", params={"rodovia": "BR-040", "tipo": "acidente"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_total(client):
    client.post("/ocorrencias", json=DADOS)
    client.post("/ocorrencias", json=DADOS)
    assert client.get("/ocorrencias/total").json() == {"total": 2}


def test_patch_altera_so_o_campo_enviado(client):
    criada = client.post("/ocorrencias", json=DADOS).json()
    resp = client.patch(f"/ocorrencias/{criada['id']}", json={"km": 15})
    assert resp.status_code == 200
    assert resp.json()["km"] == 15
    assert resp.json()["rodovia"] == "BR-040"


def test_deletar(client):
    criada = client.post("/ocorrencias", json=DADOS).json()
    assert client.delete(f"/ocorrencias/{criada['id']}").status_code == 204
    assert client.get(f"/ocorrencias/{criada['id']}").status_code == 404


@pytest.mark.parametrize("limite", [0, 51])
def test_limite_fora_do_intervalo_retorna_422(client, limite):
    assert client.get("/ocorrencias", params={"limite": limite}).status_code == 422