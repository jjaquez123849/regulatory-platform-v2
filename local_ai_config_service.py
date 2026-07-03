from pathlib import Path

from sqlalchemy.orm import Session

from app.models.local_ai_config import LocalAIModelConfig


def create_local_ai_model(db: Session, data: dict) -> LocalAIModelConfig:
    if data.get("is_default"):
        db.query(LocalAIModelConfig).update({"is_default": False})

    item = LocalAIModelConfig(**data)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def list_local_ai_models(db: Session) -> list[LocalAIModelConfig]:
    return (
        db.query(LocalAIModelConfig)
        .order_by(LocalAIModelConfig.created_at.desc())
        .all()
    )


def get_default_local_ai_model(db: Session) -> LocalAIModelConfig | None:
    return (
        db.query(LocalAIModelConfig)
        .filter(
            LocalAIModelConfig.is_default == True,
            LocalAIModelConfig.is_active == True,
        )
        .first()
    )


def get_local_ai_model(
    db: Session,
    model_id: int | None = None,
) -> LocalAIModelConfig | None:
    if model_id:
        return (
            db.query(LocalAIModelConfig)
            .filter(
                LocalAIModelConfig.id == model_id,
                LocalAIModelConfig.is_active == True,
            )
            .first()
        )

    return get_default_local_ai_model(db)


def check_local_model_available(config: LocalAIModelConfig | None) -> dict:
    if not config:
        return {
            "available": False,
            "reason": "No hay modelo local configurado.",
        }

    if config.engine_type == "rule_based":
        return {
            "available": True,
            "reason": "Motor basado en reglas disponible.",
        }

    if not config.model_path:
        return {
            "available": False,
            "reason": "No se configuró ruta del modelo.",
        }

    model_path = Path(config.model_path)

    if not model_path.exists():
        return {
            "available": False,
            "reason": f"El archivo/carpeta del modelo no existe: {config.model_path}",
        }

    return {
        "available": True,
        "reason": "Modelo local encontrado.",
    }
