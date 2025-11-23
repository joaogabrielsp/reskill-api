from typing import Optional
from sqlalchemy.orm import Session

from app.models.database import Usuario, qualidades_to_json, qualidades_from_json
from app.schemas.pydantic import UsuarioCreate, UsuarioUpdate, UsuarioResponse, MessageResponse, RoadmapResponse, RoadmapStepUpdate
from app.services.ai_roadmap import gerar_roadmap_ai


class Service:

    @staticmethod
    def create_user(dados: UsuarioCreate, db: Session) -> UsuarioResponse:
        if not dados.name or len(dados.name.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")

        if not dados.email or "@" not in dados.email:
            raise ValueError("Email inválido")

        if not dados.currentProfession:
            raise ValueError("Profissão é obrigatória")

        if Service._email_existe(dados.email, db):
            raise ValueError("Email já cadastrado no sistema")

        usuario_db = Usuario(
            nome=dados.name.strip(),
            email=dados.email.lower().strip(),
            senha_hash="hash_fake",
            profissao=dados.currentProfession,
            nivel_experience=dados.experienceLevel,
            tempo_estudo_semanal=dados.weeklyStudyTime,
            interesses=dados.interests or "",
            qualidades=qualidades_to_json(getattr(dados, 'qualities', [])),
        )

        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)

        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def get_user(user_id: int, db: Session) -> UsuarioResponse:
        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_db:
            raise ValueError("Usuário não encontrado")

        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def update_user(user_id: int, dados: UsuarioUpdate, db: Session) -> UsuarioResponse:
        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_db:
            raise ValueError("Usuário não encontrado")

        if dados.name is not None:
            if len(dados.name.strip()) < 2:
                raise ValueError("Nome deve ter pelo menos 2 caracteres")
            usuario_db.nome = dados.name.strip()

        if dados.currentProfession is not None:
            if len(dados.currentProfession.strip()) < 2:
                raise ValueError("Profissão deve ter pelo menos 2 caracteres")
            usuario_db.profissao = dados.currentProfession.strip()

        if dados.qualidades is not None:
            if not isinstance(dados.qualidades, list):
                raise ValueError("Qualidades deve ser uma lista")

            qualidades_validas = [q.strip() for q in dados.qualidades if q.strip()]
            usuario_db.qualidades = qualidades_to_json(qualidades_validas)

        db.commit()
        db.refresh(usuario_db)

        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def delete_user(user_id: int, db: Session) -> MessageResponse:
        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_db:
            raise ValueError("Usuário não encontrado")

        db.delete(usuario_db)
        db.commit()

        return MessageResponse(message="Usuário deletado com sucesso", success=True)

    @staticmethod
    def get_roadmap(user_id: int, db: Session) -> RoadmapResponse:
        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario:
            raise ValueError("Usuário não encontrado")

        roadmap_gerado = gerar_roadmap_ai(usuario)

        roadmap_com_status = Service._verificar_status_steps(
            roadmap_gerado, user_id, db
        )

        return RoadmapResponse(roadmapSteps=roadmap_com_status)

    @staticmethod
    def _verificar_status_steps(roadmap_steps: list, user_id: int, db: Session) -> list:
        from app.models.database import StatusStep

        status_steps = db.query(StatusStep).filter(
            StatusStep.id_usuario == user_id
        ).all()

        status_map = {}
        for status in status_steps:
            status_map[str(status.id_step)] = status.status.value

        for step in roadmap_steps:
            step_id = step["id"]
            if step_id in status_map:
                step["completed"] = status_map[step_id] == "concluido"
            else:
                step["completed"] = False

        return roadmap_steps

    @staticmethod
    def _email_existe(email: str, db: Session) -> bool:
        if not email:
            return False
        return db.query(Usuario).filter(Usuario.email == email.lower().strip()).first() is not None

    @staticmethod
    def _format_usuario_response(usuario_db) -> UsuarioResponse:
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
        if not email:
            return None

        usuario_db = db.query(Usuario).filter(Usuario.email == email.lower().strip()).first()
        if not usuario_db:
            return None

        return Service._format_usuario_response(usuario_db)

    @staticmethod
    def toggle_step_status(user_id: int, step_id: int, dados: RoadmapStepUpdate, db: Session) -> MessageResponse:
        if not dados.status:
            raise ValueError("Status é obrigatório")

        if not user_id or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario:
            raise ValueError("Usuário não encontrado")

        from app.models.database import StatusStep, StatusStepEnum

        status_step = db.query(StatusStep).filter(
            StatusStep.id_usuario == user_id,
            StatusStep.id_step == step_id
        ).first()

        if status_step:
            status_step.status = StatusStepEnum(dados.status.value)
        else:
            status_step = StatusStep(
                id_usuario=user_id,
                id_step=step_id,
                descricao=f"Status do step {step_id}",
                status=StatusStepEnum(dados.status.value)
            )
            db.add(status_step)

        db.commit()
        return MessageResponse(message="Status atualizado com sucesso", success=True)