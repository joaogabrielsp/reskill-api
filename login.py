from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

# ----------------- CONFIG JWT -----------------

SECRET_KEY = "global_solutions_2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ----------------- APP & CORS -----------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # pra projeto de faculdade, OK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- MODELOS -----------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: EmailStr

class CurrentUser(BaseModel):
    email: EmailStr
    name: str

# ----------------- MOCK USERS -----------------

MOCK_USERS = {
    "aluno@fiap.com": {
        "password": "123456",
        "name": "Aluno FIAP",
    },
    "nath@example.com": {
        "password": "senhaSegura",
        "name": "Nath",
    },
}

# ----------------- FUNÇÃO PRA CRIAR TOKEN -----------------

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----------------- LOGIN -----------------

@app.post("/", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = MOCK_USERS.get(payload.email)

    if not user or payload.password != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token({"sub": payload.email})

    return LoginResponse(
        access_token=access_token,
        name=user["name"],
        email=payload.email,
    )

# ----------------- DEPENDÊNCIA QUE VALIDA O TOKEN -----------------

def get_current_user(authorization: str = Header(None)) -> CurrentUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não enviado",
        )

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None or email not in MOCK_USERS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    user = MOCK_USERS[email]
    return CurrentUser(email=email, name=user["name"])

# ----------------- ROTA PROTEGIDA DE EXEMPLO -----------------

@app.get("/me", response_model=CurrentUser)
def read_me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("login:app", host="127.0.0.1", port=8000, reload=True)
