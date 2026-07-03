from sqlalchemy.orm import Session

from app.services.local_ai_config_service import (
    check_local_model_available,
    get_local_ai_model,
)


class LocalAIOrchestrator:
    def __init__(self, db: Session):
        self.db = db

    def test_prompt(
        self,
        prompt: str,
        model_id: int | None = None,
    ) -> dict:
        config = get_local_ai_model(self.db, model_id)
        health = check_local_model_available(config)

        if not config:
            return {
                "engine_type": "none",
                "available": False,
                "response": health["reason"],
            }

        if config.engine_type == "rule_based":
            return {
                "engine_type": config.engine_type,
                "available": True,
                "response": self._rule_based_response(prompt),
            }

        if not health["available"]:
            return {
                "engine_type": config.engine_type,
                "available": False,
                "response": health["reason"],
            }

        return {
            "engine_type": config.engine_type,
            "available": False,
            "response": (
                "El modelo fue localizado, pero el motor de ejecución local "
                "se conectará en el próximo paquete."
            ),
        }

    def _rule_based_response(self, prompt: str) -> str:
        clean = " ".join(prompt.split())

        if len(clean) <= 500:
            return f"Respuesta rule_based: {clean}"

        return f"Respuesta rule_based: {clean[:500]}..."
