from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum
import json


class StatusStepEnum(str, Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"


class UsuarioCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    currentProfession: str = Field(..., min_length=2, max_length=100, description="Profissão atual")
    experienceLevel: str = Field(..., description="Nível de experiência: iniciante, intermediario, avancado ou experiente")
    weeklyStudyTime: float = Field(..., gt=0, le=50, description="Horas de estudo por semana (mínimo 1, máximo 50)")
    interests: str = Field(..., max_length=500, description="Áreas de interesse")
    qualities: List[str] = Field(default=[], description="Lista de qualidades do usuário")

    class Config:
        schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao@email.com",
                "currentProfession": "Operador de Caixa",
                "experienceLevel": "iniciante",
                "weeklyStudyTime": 5.0,
                "interests": "Tecnologia, Gestão de Projetos",
                "qualities": ["Dedicado", "Proativo"]
            }
        }


class UsuarioUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome do usuário")
    currentProfession: Optional[str] = Field(None, min_length=2, max_length=100, description="Profissão atual")
    qualities: Optional[List[str]] = Field(None, description="Lista de qualidades do usuário")

    class Config:
        schema_extra = {
            "example": {
                "name": "João Silva Atualizado",
                "qualities": ["Dedicado", "Proativo", "Organizado"]
            }
        }


class RoadmapStepCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, description="Título da etapa personalizada")
    description: str = Field(..., max_length=500, description="Descrição detalhada da etapa")

    class Config:
        schema_extra = {
            "example": {
                "title": "Fazer curso de React avançado",
                "description": "Curso na Udemy focado em hooks e performance"
            }
        }


class RoadmapStepUpdate(BaseModel):
    status: Optional[StatusStepEnum] = Field(None, description="Novo status: pendente, em_andamento ou concluido")

    class Config:
        schema_extra = {
            "example": {
                "status": "concluido"
            }
        }


class UsuarioResponse(BaseModel):
    id: int
    name: str
    email: str
    currentProfession: str
    experienceLevel: str
    weeklyStudyTime: float
    interests: str
    qualities: List[str]

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao@email.com",
                "currentProfession": "Operador de Caixa",
                "experienceLevel": "iniciante",
                "weeklyStudyTime": 5.0,
                "interests": "Tecnologia, Gestão de Projetos",
                "qualities": ["Dedicado", "Proativo"]
            }
        }


class RoadmapStepResponse(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    order: int

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Desenvolver Habilidades Técnicas",
                "description": "Fazer cursos online em plataformas reconhecidas",
                "completed": False,
                "order": 2
            }
        }


class RoadmapResponse(BaseModel):
    roadmapSteps: List[RoadmapStepResponse]

    class Config:
        schema_extra = {
            "example": {
                "roadmapSteps": [
                    {
                        "id": "1",
                        "title": "Autoconhecimento e Análise de Mercado",
                        "description": "Pesquisar tendências e identificar áreas em crescimento",
                        "completed": True,
                        "order": 1
                    },
                    {
                        "id": "2",
                        "title": "Desenvolver Habilidades Técnicas",
                        "description": "Fazer cursos online em plataformas reconhecidas",
                        "completed": False,
                        "order": 2
                    }
                ]
            }
        }


class MessageResponse(BaseModel):
    message: str
    success: bool = True

    class Config:
        schema_extra = {
            "example": {
                "message": "Usuário criado com sucesso!",
                "success": True
            }
        }


class ErrorResponse(BaseModel):
    message: str
    success: bool = False
    error_code: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Email já cadastrado no sistema",
                "success": False,
                "error_code": "EMAIL_EXISTS"
            }
        }