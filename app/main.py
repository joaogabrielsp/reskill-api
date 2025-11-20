from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import (
    get_db,
    create_tables,
    Usuario,
    qualidades_to_json,
    qualidades_from_json,
)
from app.schemas.pydantic import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    MessageResponse,
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.on_event("startup")
def on_startup():
    # Garante que as tabelas existem
    create_tables()


# ========= 1) POST - criar usuário =========
@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )

    novo_usuario = Usuario(
        nome=dados.name,
        email=dados.email,
        senha_hash="hash_fake_por_enquanto",  # só pra não quebrar
        profissao=dados.currentProfession,
        nivel_experience=dados.experienceLevel,
        tempo_estudo_semanal=dados.weeklyStudyTime,
        interesses=dados.interests,
        qualidades=qualidades_to_json(dados.qualities),
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Monta resposta no formato esperado pelo frontend
    return UsuarioResponse(
        id=novo_usuario.id,
        name=novo_usuario.nome,
        email=novo_usuario.email,
        currentProfession=novo_usuario.profissao,
        experienceLevel=novo_usuario.nivel_experience,
        weeklyStudyTime=novo_usuario.tempo_estudo_semanal,
        interests=novo_usuario.interesses,
        qualities=qualidades_from_json(novo_usuario.qualidades),
    )


# ========= 2) GET - buscar usuário por id =========
@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    return UsuarioResponse(
        id=usuario_db.id,
        name=usuario_db.nome,
        email=usuario_db.email,
        currentProfession=usuario_db.profissao,
        experienceLevel=usuario_db.nivel_experience,
        weeklyStudyTime=usuario_db.tempo_estudo_semanal,
        interests=usuario_db.interesses,
        qualities=qualidades_from_json(usuario_db.qualidades),
    )


# ========= 3) PUT - atualizar usuário (update parcial) =========
@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Só atualiza o que veio no body
    if dados.name is not None:
        usuario_db.nome = dados.name
    if dados.currentProfession is not None:
        usuario_db.profissao = dados.currentProfession
    if dados.qualities is not None:
        usuario_db.qualidades = qualidades_to_json(dados.qualities)

    db.commit()
    db.refresh(usuario_db)

    return UsuarioResponse(
        id=usuario_db.id,
        name=usuario_db.nome,
        email=usuario_db.email,
        currentProfession=usuario_db.profissao,
        experienceLevel=usuario_db.nivel_experience,
        weeklyStudyTime=usuario_db.tempo_estudo_semanal,
        interests=usuario_db.interesses,
        qualities=qualidades_from_json(usuario_db.qualidades),
    )


# ========= 4) DELETE - remover usuário =========
@app.delete("/usuarios/{usuario_id}", response_model=MessageResponse)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    db.delete(usuario_db)
    db.commit()

    return MessageResponse(message="Usuário deletado com sucesso", success=True)
