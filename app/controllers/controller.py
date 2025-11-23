"""
Controllers - Camada HTTP

Responsável por:
- Receber requisições HTTP
- Validar dados de entrada
- Chamar services (lógica de negócio)
- Retornar respostas HTTP
- Tratar erros HTTP
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.pydantic import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse, MessageResponse
)
from app.services.service import Service


# ========= 1) POST - create user =========
def create_user(dados: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.

    Endpoint: POST /users
    """
    try:
        print(f"DADOS RECEBIDOS: {dados}")
        print(f"ATRIBUTOS: {dir(dados)}")
        if hasattr(dados, 'qualities'):
            print(f"QUALITIES: {dados.qualities}")
        else:
            print("QUALITIES NÃO EXISTE!")
        return Service.create_user(dados, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"ERRO DETALHADO: {str(e)}")
        print(f"TIPO ERRO: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


# ========= 2) GET - get user by id =========
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Busca usuário por ID.

    Endpoint: GET /users/{user_id}
    """
    try:
        return Service.get_user(user_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor"
        )


# ========= 3) PUT - update user =========
def update_user(user_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    """
    Atualiza dados do usuário.

    Endpoint: PUT /users/{user_id}
    """
    try:
        return Service.update_user(user_id, dados, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor"
        )


# ========= 4) DELETE - delete user =========
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Remove um usuário do sistema.

    Endpoint: DELETE /users/{user_id}
    """
    try:
        return Service.delete_user(user_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor"
        )