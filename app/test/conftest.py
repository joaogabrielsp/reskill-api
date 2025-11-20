# tests/conftest.py
import json
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.models.database import Base, Usuario, get_db, qualidades_to_json


# Banco de teste (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_reskill.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override da dependência do FastAPI
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Cria as tabelas no banco de teste
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_usuarios(db_session):
    """
    Carrega usuários mockados do arquivo JSON e insere direto no banco.
    """
    db_session.query(Usuario).delete()
    db_session.commit()

    file_path = os.path.join(os.path.dirname(__file__), "mock_usuarios.json")
    with open(file_path, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    created = []
    for u in usuarios:
        usuario_db = Usuario(
            nome=u["name"],
            email=u["email"],
            senha_hash="hash_teste",
            profissao=u["currentProfession"],
            nivel_experience=u["experienceLevel"],
            tempo_estudo_semanal=u["weeklyStudyTime"],
            interesses=u["interests"],
            qualidades=qualidades_to_json(u["qualities"]),
        )
        db_session.add(usuario_db)
        created.append(usuario_db)

    db_session.commit()

    # Refresh pra garantir que IDs foram gerados
    for u in created:
        db_session.refresh(u)

    return created
