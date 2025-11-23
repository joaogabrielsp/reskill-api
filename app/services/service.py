"""
Services - Camada de Lógica de Negócio

Responsável por:
- Validações de negócio
- Regras específicas da aplicação
- Chamadas ao model (data access)
- Formatação de respostas
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.database import Usuario, qualidades_to_json, qualidades_from_json
from app.schemas.pydantic import UsuarioCreate, UsuarioUpdate, UsuarioResponse, MessageResponse


class Service:
    """Service central com toda lógica de negócio."""

    @staticmethod
    def create_user(dados: UsuarioCreate, db: Session) -> UsuarioResponse:
        """
        Cria um novo usuário no sistema com validações de negócio.

        Regras:
        - Email não pode existir
        - Todos os campos obrigatórios devem estar presentes
        """
        # 1. Validações de negócio
        if not dados.name or len(dados.name.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")

        if not dados.email or "@" not in dados.email:
            raise ValueError("Email inválido")

        if not dados.currentProfession:
            raise ValueError("Profissão é obrigatória")

        # 2. Verificação de unicidade
        if Service._email_existe(dados.email, db):
            raise ValueError("Email já cadastrado no sistema")

        # 3. Criar usuário
        usuario_db = Usuario(
            nome=dados.name.strip(),
            email=dados.email.lower().strip(),
            senha_hash="hash_fake",  # TODO: Implementar hashing real com bcrypt
            profissao=dados.currentProfession,
            nivel_experience=dados.experienceLevel,
            tempo_estudo_semanal=dados.weeklyStudyTime,
            interesses=dados.interests or "",
            qualidades=qualidades_to_json(getattr(dados, 'qualities', [])),
        )

        # 4. Salvar no banco
        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)

        # 5. Retornar resposta formatada
        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def get_user(user_id: int, db: Session) -> UsuarioResponse:
        """
        Busca usuário por ID com validações.
        """
        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_db:
            raise ValueError("Usuário não encontrado")

        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def update_user(user_id: int, dados: UsuarioUpdate, db: Session) -> UsuarioResponse:
        """
        Atualiza dados do usuário com validações.
        """
        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_db:
            raise ValueError("Usuário não encontrado")

        # Só atualiza campos que foram fornecidos
        if dados.name is not None:
            if len(dados.name.strip()) < 2:
                raise ValueError("Nome deve ter pelo menos 2 caracteres")
            usuario_db.nome = dados.name.strip()

        if dados.currentProfession is not None:
            if len(dados.currentProfession.strip()) < 2:
                raise ValueError("Profissão deve ter pelo menos 2 caracteres")
            usuario_db.profissao = dados.currentProfession.strip()

        if dados.qualidades is not None:
            # Validar que qualidades seja uma lista de strings válidas
            if not isinstance(dados.qualidades, list):
                raise ValueError("Qualidades deve ser uma lista")

            # Remover strings vazias e espaços
            qualidades_validas = [q.strip() for q in dados.qualidades if q.strip()]
            usuario_db.qualidades = qualidades_to_json(qualidades_validas)

        db.commit()
        db.refresh(usuario_db)

        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def delete_user(user_id: int, db: Session) -> MessageResponse:
        """
        Remove um usuário com validações de segurança.
        """
        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_db:
            raise ValueError("Usuário não encontrado")

        # TODO: Verificar se usuário tem dependências antes de deletar
        # (ex: roadmaps, etapas concluídas, etc.)

        db.delete(usuario_db)
        db.commit()

        return MessageResponse(message="Usuário deletado com sucesso", success=True)

    @staticmethod
    def _email_existe(email: str, db: Session) -> bool:
        """Verifica se email já existe no sistema."""
        if not email:
            return False
        return db.query(Usuario).filter(Usuario.email == email.lower().strip()).first() is not None

    @staticmethod
    def _format_usuario_response(usuario_db) -> UsuarioResponse:
        """
        Formata objeto do banco para response do frontend.
        """
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

    @staticmethod
    def get_usuario_por_email(email: str, db: Session) -> Optional[UsuarioResponse]:
        """
        Busca usuário por email (útil para validações).
        """
        if not email:
            return None

        usuario_db = db.query(Usuario).filter(Usuario.email == email.lower().strip()).first()
        if not usuario_db:
            return None

        return Service._format_usuario_response(usuario_db)