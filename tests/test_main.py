from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

@pytest.fixture
def user_data():
    return {"username": "testeuser", "password": "senha123"}

def test_cadastro_usuario(user_data):
    response = client.post("/cadastro", json=user_data)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert "id" in response.json()
        assert response.json()["username"] == user_data["username"]

def test_login_usuario(user_data):
    response = client.post("/login", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]

def test_me_usuario(user_data):
    token = test_login_usuario(user_data)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]
