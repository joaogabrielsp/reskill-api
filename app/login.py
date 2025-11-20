from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import bcrypt
from fastapi import Depends

# ----------------- CONFIG JWT -----------------

SECRET_KEY = "global_solutions_2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ----------------- APP & CORS -----------------

app = FastAPI()
security = HTTPBearer()

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
    role: str

class CurrentUser(BaseModel):
    email: EmailStr
    name: str
    role: str

# ----------------- MOCK USERS -----------------

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

MOCK_USERS = {
    "aluno@fiap.com": {
        "password_hash": hash_password("123456"),
        "name": "Aluno FIAP",
        "role": "user"
    },
    "admin@fiap.com": {
        "password_hash": hash_password("senhaSegura"),
        "name": "Admin",
        "role": "admin"
    },
}

# ----------------- FUNÇÃO PRA CRIAR TOKEN -----------------

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----- SENHA ----
def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))

# ----------------- LOGIN -----------------

@app.post("/", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = MOCK_USERS.get(payload.email)

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token({
        "sub": payload.email,
        "role": user["role"]
    })

    return LoginResponse(
        access_token=access_token,
        name=user["name"],
        email=payload.email,
        role=user["role"],
    )

# ----------------- DEPENDÊNCIA QUE VALIDA O TOKEN -----------------

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Token não enviado"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        if email is None or role is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    user = MOCK_USERS[email]
    return CurrentUser(email=email, name=user["name"], role=role)


def require_admin(current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido somente para administradores"
        )
    return current_user

@app.get("/admin-only")
def admin_dashboard(user: CurrentUser = Depends(require_admin)):
    return {"message": "Bem-vindo, admin!", "user": user}



# ----------------- ROTA PROTEGIDA DE EXEMPLO -----------------

@app.get("/me", response_model=CurrentUser)
def read_me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user

@app.get("/profile")
def profile(user: CurrentUser = Depends(get_current_user)):
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("login:app", host="127.0.0.1", port=8000, reload=True)
