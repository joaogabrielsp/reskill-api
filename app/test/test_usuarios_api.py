# tests/test_usuarios_api.py
from sqlalchemy.orm import Session
from app.models.database import Usuario, qualidades_from_json


# ========= 1) POST =========
def test_criar_usuario(client):
    payload = {
        "name": "Novo Usuario",
        "email": "novo@example.com",
        "currentProfession": "Estudante",
        "experienceLevel": "iniciante",
        "weeklyStudyTime": 6,
        "interests": "Backend, APIs",
        "qualities": ["Curioso", "Persistente"]
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["currentProfession"] == payload["currentProfession"]
    assert data["qualities"] == payload["qualities"]


# ========= 2) GET =========
def test_obter_usuario(client, mock_usuarios):
    usuario = mock_usuarios[0]

    response = client.get(f"/users/{usuario.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario.id
    assert data["name"] == usuario.nome
    assert data["email"] == usuario.email


# ========= 3) PUT (update parcial) =========
def test_atualizar_usuario(client, mock_usuarios):
    usuario = mock_usuarios[1]

    payload = {
        "name": "Nome Atualizado",
        "qualities": ["Dedicado", "Organizado"]
    }

    response = client.put(f"/users/{usuario.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario.id
    assert data["name"] == payload["name"]
    assert data["qualities"] == payload["qualities"]


# ========= 4) DELETE =========
def test_deletar_usuario(client, mock_usuarios):
    usuario = mock_usuarios[0]

    # Deleta
    response = client.delete(f"/users/{usuario.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True

    # Tenta buscar depois → 404
    response_get = client.get(f"/users/{usuario.id}")
    assert response_get.status_code == 404
