from sqlalchemy.orm import Session

from app.engines.local_ai.local_ai_orchestrator import LocalAIOrchestrator
from app.services.workspace_service import get_record_workspace


def build_workspace_ai_prompt(workspace: dict) -> str:
    record = workspace.get("record", {})
    documents = workspace.get("documents", [])
    people = workspace.get("people", [])
    request_items = workspace.get("request_items", [])
    quality = workspace.get("quality", {})
    comments = workspace.get("comments", [])

    return f"""
Analiza el siguiente expediente regulatorio y responde en español claro.

Debes producir:
1. Resumen ejecutivo.
2. Riesgos o alertas.
3. Información faltante.
4. Próximas acciones recomendadas.

Expediente:
ID: {record.get("id")}
Título: {record.get("title")}
Resumen actual: {record.get("summary")}
Estado: {record.get("state")}
Pendientes: {record.get("has_pending_items")}

Personas:
{people}

Solicitudes:
{request_items}

Documentos:
{documents}

Calidad:
{quality}

Comentarios:
{comments}
""".strip()


def run_workspace_ai_analysis(
    db: Session,
    record_id: int,
    current_user
) -> dict:
    workspace = get_record_workspace(
        db=db,
        record_id=record_id,
        current_user=current_user
    )

    prompt = build_workspace_ai_prompt(workspace)

    orchestrator = LocalAIOrchestrator(db)

    result = orchestrator.test_prompt(
        prompt=prompt,
        model_id=None
    )

    return {
        "record_id": record_id,
        "engine_type": result.get("engine_type"),
        "available": result.get("available"),
        "analysis": result.get("response"),
    }
