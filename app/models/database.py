from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Enum, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from enum import Enum as PyEnum
import os
import json

# Configuração do Banco SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reskill.db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Enum para Status do Step
class StatusStepEnum(PyEnum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"


class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    profissao = Column(String(100), nullable=False)
    nivel_experience = Column(String(100), nullable=False)
    tempo_estudo_semanal = Column(Double, nullable=False)
    interesses = Column(String(255), nullable=False)
    qualidades = Column(String(255), nullable=False)  # JSON string: '["Dedicado", "Proativo"]'

    # Relacionamentos
    usuario_steps = relationship("UsuarioStep", back_populates="usuario", cascade="all, delete-orphan")
    status_steps = relationship("StatusStep", back_populates="usuario", cascade="all, delete-orphan")


class Steps(Base):
    __tablename__ = "Steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(100), nullable=False)

    # Relacionamentos
    usuario_steps = relationship("UsuarioStep", back_populates="step")
    status_steps = relationship("StatusStep", back_populates="step")


class UsuarioStep(Base):
    __tablename__ = "UsuarioStep"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("Usuario.id"), nullable=False)
    id_step = Column(Integer, ForeignKey("Steps.id"), nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="usuario_steps")
    step = relationship("Steps", back_populates="usuario_steps")


class StatusStep(Base):
    __tablename__ = "StatusStep"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("Usuario.id"), nullable=False)
    id_step = Column(Integer, ForeignKey("Steps.id"), nullable=False)
    descricao = Column(String(100), nullable=False)
    status = Column(Enum(StatusStepEnum), nullable=False, default=StatusStepEnum.PENDENTE)
    data_conclusao = Column(Date, nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="status_steps")
    step = relationship("Steps", back_populates="status_steps")


# Função para criar as tabelas
def create_tables():
    Base.metadata.create_all(bind=engine)


# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Criar steps padrão (mockados)
def criar_steps_padrao(db):
    steps_padrao = [
        {
            "nome": "Autoconhecimento e Análise de Mercado",
            "descricao": "Pesquisar tendências e identificar áreas em crescimento"
        },
        {
            "nome": "Desenvolver Habilidades Técnicas",
            "descricao": "Fazer cursos online em plataformas reconhecidas"
        },
        {
            "nome": "Construir Portfólio Digital",
            "descricao": "Criar projetos práticos que demonstrem suas habilidades"
        },
        {
            "nome": "Networking Estratégico",
            "descricao": "Conectar-se com profissionais da área desejada"
        },
        {
            "nome": "Certificações Relevantes",
            "descricao": "Obter certificações reconhecidas no mercado"
        },
        {
            "nome": "Otimizar Currículo e LinkedIn",
            "descricao": "Atualizar documentos profissionais"
        },
        {
            "nome": "Aplicar para Vagas Estratégicas",
            "descricao": "Candidatar-se a posições compatíveis com seu perfil"
        }
    ]

    for step_data in steps_padrao:
        step_existente = db.query(Steps).filter(Steps.nome == step_data["nome"]).first()
        if not step_existente:
            novo_step = Steps(**step_data)
            db.add(novo_step)

    db.commit()


# Funções auxiliares para qualidades
def qualidades_to_json(qualidades_list: list) -> str:
    return json.dumps(qualidades_list, ensure_ascii=False)


def qualidades_from_json(qualidades_str: str) -> list:
    try:
        return json.loads(qualidades_str)
    except (json.JSONDecodeError, TypeError):
        return []