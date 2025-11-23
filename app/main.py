from fastapi import FastAPI, Depends
from app.models.database import create_tables, get_db
from app.schemas.pydantic import UsuarioCreate, UsuarioUpdate, UsuarioResponse, MessageResponse, RoadmapResponse, RoadmapStepUpdate
from app.controllers.controller import (
    create_user,
    get_user,
    update_user,
    delete_user,
    get_roadmap,
    toggle_step_status,
)

app = FastAPI(title="ReSkill API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "ReSkill API - Version 1.0.0"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/users", response_model=UsuarioResponse, status_code=201)
def endpoint_create_user(dados: UsuarioCreate, db = Depends(get_db)):
    return create_user(dados, db)

@app.get("/users/{user_id}", response_model=UsuarioResponse)
def endpoint_get_user(user_id: int, db = Depends(get_db)):
    return get_user(user_id, db)

@app.put("/users/{user_id}", response_model=UsuarioResponse)
def endpoint_update_user(user_id: int, dados: UsuarioUpdate, db = Depends(get_db)):
    return update_user(user_id, dados, db)

@app.delete("/users/{user_id}", response_model=MessageResponse)
def endpoint_delete_user(user_id: int, db = Depends(get_db)):
    return delete_user(user_id, db)

@app.get("/roadmap", response_model=RoadmapResponse)
def endpoint_get_roadmap(user_id: int, db = Depends(get_db)):
    return get_roadmap(user_id, db)

@app.put("/roadmap/steps/{step_id}/toggle", response_model=MessageResponse)
def endpoint_toggle_step_status(step_id: int, user_id: int, dados: RoadmapStepUpdate, db = Depends(get_db)):
    return toggle_step_status(user_id, step_id, dados, db)