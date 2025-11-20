"""
Schemas Pydantic para validação e serialização de dados.

Este arquivo define as "regras" para dados que entram e saem da nossa API.
Pydantic vai garantir que só dados corretos passem!
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum
import json


# ===== ENUMS (Valores exatos permitidos) =====
"""
Enums definem lista de valores permitidos para um campo.
Impede que mandem valores inválidos como "status: 'azul'".
"""

class StatusStepEnum(str, Enum):
    """
    Valores permitidos para status de uma etapa do roadmap.
    Se frontend mandar outro valor → Pydantic barra automaticamente!
    """
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"


# ===== REQUEST SCHEMAS (Dados que CHEGAM do frontend) =====
"""
Esses schemas validam JSON que vem do navegador.
Se algo estiver errado → erro automático com mensagem clara!
"""

class UsuarioCreate(BaseModel):
    """
    Schema para criar novo usuário.
    Valida os dados do formulário de cadastro.

    Por que usar? Para garantir que:
    - Nome não seja vazio nem muito longo
    - Email tenha formato válido
    - Tempo de estudo seja número (não texto)
    - Qualidades seja lista (não texto)
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    currentProfession: str = Field(..., min_length=2, max_length=100, description="Profissão atual")
    experienceLevel: str = Field(..., description="Nível de experiência: iniciante, intermediario, avancado ou experiente")
    weeklyStudyTime: float = Field(..., gt=0, le=50, description="Horas de estudo por semana (mínimo 1, máximo 50)")
    interests: str = Field(..., max_length=500, description="Áreas de interesse")
    qualities: List[str] = Field(default=[], description="Lista de qualidades do usuário")

    class Config:
        # Documentação automática via OpenAPI/Swagger
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
    """
    Schema para atualizar dados do usuário.

    Importante: Campos são Optional porque usuário pode querer
    atualizar só o nome, só as qualidades, ou só a profissão.
    Se fossem obrigatórios, teria que mandar todos sempre!
    """
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
    """
    Schema para quando usuário adiciona etapa personalizada no roadmap.

    Frontend permite criar steps além dos 7 padrões.
    Ex: "Fazer curso específico de React"
    """
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
    """
    Schema para atualizar status de uma etapa existente.

    Usado quando usuário clica para marcar etapa como concluída
    ou voltar para pendente.
    """
    status: Optional[StatusStepEnum] = Field(None, description="Novo status: pendente, em_andamento ou concluido")

    class Config:
        schema_extra = {
            "example": {
                "status": "concluido"
            }
        }


# ===== RESPONSE SCHEMAS (Dados que SAEM para o frontend) =====
"""
Esses schemas formatam dados que vamos enviar para o navegador.
Converte nomes do banco para nomes que frontend espera.
"""

class UsuarioResponse(BaseModel):
    """
    Schema para resposta de usuário ao frontend.

    Importante: Usamos Field(..., alias="nome_banco") para traduzir
    nomes do banco para nomes do frontend automaticamente!
    """
    id: int
    name: str
    email: str
    currentProfession: str
    experienceLevel: str
    weeklyStudyTime: float
    interests: str
    qualities: List[str]

    class Config:
        # Permite criar response a partir de objetos SQLAlchemy
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
    """
    Schema para resposta de etapa do roadmap.

    Formata exatamente como frontend UserContext espera.
    Importante: 'completed' é boolean (não string do banco!).
    """
    id: str  # ID como string porque frontend usa string
    title: str  # Nome do step
    description: str  # Descrição do step
    completed: bool  # true/false baseado no status
    order: int = Field(..., alias="ordem")  # banco.ordem → frontend.order

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
    """
    Schema para resposta completa do roadmap.

    Retorna todas as etapas do usuário em um único objeto,
    formato que frontend UserContext espera.
    """
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


# ===== MENSAGENS PADRÃO (Respostas simples) =====
"""
Schemas para respostas de sucesso/erro padrão da API.
Ajuda a ter respostas consistentes em todos endpoints.
"""

class MessageResponse(BaseModel):
    """Resposta padrão de mensagens de sucesso"""
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
    """Resposta padrão de erros da API"""
    message: str
    success: bool = False
    error_code: Optional[str] = None  # Código do erro para tratamento no frontend

    class Config:
        schema_extra = {
            "example": {
                "message": "Email já cadastrado no sistema",
                "success": False,
                "error_code": "EMAIL_EXISTS"
            }
        }