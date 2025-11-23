from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.pydantic import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse, MessageResponse, RoadmapResponse, RoadmapStepUpdate
)
from app.services.service import Service


def create_user(dados: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return Service.create_user(dados, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


def get_user(user_id: int, db: Session = Depends(get_db)):
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


def update_user(user_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
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


def delete_user(user_id: int, db: Session = Depends(get_db)):
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


def get_roadmap(user_id: int, db: Session = Depends(get_db)):
    try:
        return Service.get_roadmap(user_id, db)
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


def toggle_step_status(user_id: int, step_id: int, dados: RoadmapStepUpdate, db: Session = Depends(get_db)):
    try:
        return Service.toggle_step_status(user_id, step_id, dados, db)
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