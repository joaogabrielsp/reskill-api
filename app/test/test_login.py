from fastapi.testclient import TestClient
from app.login import app, SECRET_KEY, ALGORITHM
from jose import jwt

client = TestClient(app)

def test_login_and_me():
    # 1. Login com usuário válido
    response = client.post("/", json={
        "email": "aluno@fiap.com",
        "password": "123456"
    })

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data

    token = data["access_token"]

    # 2. O token realmente é um JWT válido?
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "aluno@fiap.com"

    # 3. Chamar rota protegida /me
    response_me = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_me.status_code == 200

    me_data = response_me.json()

    assert me_data["email"] == "aluno@fiap.com"
    assert me_data["name"] == "Aluno FIAP"
