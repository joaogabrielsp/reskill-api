from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- MODELOS -----
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: EmailStr

# ----- DADOS MOCKADOS -----
MOCK_USERS = {
    "aluno@fiap.com": {
        "password": "123456",   # em produção isso seria hash
        "name": "Aluno FIAP",
    },
    "nath@example.com": {
        "password": "senhaSegura",
        "name": "Nath",
    },
}

# ----- ENDPOINT DE LOGIN -----
@app.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = MOCK_USERS.get(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if payload.password != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Token fake só pro TCC (pode ser qualquer string)
    fake_token = f"fake-token-for-{payload.email}"

    return LoginResponse(
        access_token=fake_token,
        name=user["name"],
        email=payload.email,
    )

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}