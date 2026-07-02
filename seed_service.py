from sqlalchemy.orm import Session

from app.services.admin_service import (
    create_process,
    create_process_field,
    create_field_option,
    list_processes
)
from app.services.document_config_service import (
    create_document_type,
    create_extraction_field,
    create_excel_mapping
)
from app.services.workflow_admin_service import (
    create_workflow_state,
    create_workflow_transition
)


def seed_regulatory_requests(db: Session) -> dict:
    existing = [
        process
        for process in list_processes(db)
        if process.code == "regulatory_requests"
    ]

    if existing:
        return {
            "status": "skipped",
            "message": "El proceso regulatory_requests ya existe.",
            "process_id": existing[0].id
        }

    process = create_process(
        db,
        {
            "code": "regulatory_requests",
            "name": "Requerimientos Regulatorios",
            "description": "Proceso configurable para gestión de requerimientos de reguladores, juzgados, tribunales y otros originadores.",
            "is_default": True
        }
    )

    fields = [
        {
            "name": "received_date",
            "label": "Fecha de recepción",
            "field_type": "date",
            "is_required": True,
            "display_order": 1
        },
        {
            "name": "request_number",
            "label": "No. de requerimiento",
            "field_type": "text",
            "is_required": False,
            "display_order": 2
        },
        {
            "name": "originator",
            "label": "Originador",
            "field_type": "text",
            "is_required": False,
            "display_order": 3
        },
        {
            "name": "origin",
            "label": "Origen",
            "field_type": "select",
            "is_required": False,
            "display_order": 4
        },
        {
            "name": "request_type",
            "label": "Tipo",
            "field_type": "multi_select",
            "is_required": False,
            "display_order": 5
        },
        {
            "name": "identification",
            "label": "Identificación",
            "field_type": "text",
            "is_required": False,
            "display_order": 6
        },
        {
            "name": "is_fully_answered",
            "label": "Respondido completo",
            "field_type": "boolean",
            "is_required": False,
            "display_order": 7
        },
        {
            "name": "pending_items",
            "label": "Pendientes",
            "field_type": "long_text",
            "is_required": False,
            "display_order": 8
        },
        {
            "name": "due_date",
            "label": "Fecha límite",
            "field_type": "date",
            "is_required": False,
            "display_order": 9
        },
        {
            "name": "summary",
            "label": "Resumen",
            "field_type": "long_text",
            "is_required": False,
            "display_order": 10
        }
    ]

    created_fields = {}

    for field_data in fields:
        field_data["process_id"] = process.id
        field = create_process_field(db, field_data)
        created_fields[field.name] = field

    origin_options = [
        ("juzgado", "Juzgado"),
        ("tribunal", "Tribunal"),
        ("regulador", "Regulador"),
        ("ministerio_publico", "Ministerio Público"),
        ("otro", "Otro")
    ]

    for index, (value, label) in enumerate(origin_options, start=1):
        create_field_option(
            db,
            {
                "field_id": created_fields["origin"].id,
                "value": value,
                "label": label,
                "display_order": index,
                "is_active": True
            }
        )

    request_type_options = [
        ("certificacion", "Certificación"),
        ("inmovilizacion", "Inmovilización"),
        ("descongelamiento", "Descongelamiento"),
        ("informacion_productos", "Información de productos"),
        ("estado_cuenta", "Estado de cuenta"),
        ("movimientos", "Movimientos"),
        ("bloqueo", "Bloqueo"),
        ("desbloqueo", "Desbloqueo"),
        ("otro", "Otro")
    ]

    for index, (value, label) in enumerate(request_type_options, start=1):
        create_field_option(
            db,
            {
                "field_id": created_fields["request_type"].id,
                "value": value,
                "label": label,
                "display_order": index,
                "is_active": True
            }
        )

    states_data = [
        ("received", "Recibido", 1, True, False),
        ("ai_extracted", "Extraído por IA", 2, False, False),
        ("analyst_validation", "Validación analista", 3, False, False),
        ("sent_to_area", "Enviado al área", 4, False, False),
        ("waiting_response", "Esperando respuesta", 5, False, False),
        ("quality_review", "Revisión de calidad", 6, False, False),
        ("pending_signature", "Pendiente firma", 7, False, False),
        ("ready_to_answer", "Listo para responder", 8, False, False),
        ("answered_partial", "Respondido parcial", 9, False, False),
        ("answered_complete", "Respondido completo", 10, False, False),
        ("closed", "Cerrado", 11, False, True)
    ]

    states = {}

    for code, name, order, is_initial, is_final in states_data:
        state = create_workflow_state(
            db,
            {
                "process_id": process.id,
                "code": code,
                "name": name,
                "display_order": order,
                "color": None,
                "is_initial": is_initial,
                "is_final": is_final,
                "is_active": True
            }
        )
        states[code] = state

    transitions_data = [
        ("extract_ai", "Extraer con IA", "received", "ai_extracted"),
        ("validate_extraction", "Validar extracción", "ai_extracted", "analyst_validation"),
        ("send_to_area", "Enviar al área", "analyst_validation", "sent_to_area"),
        ("mark_waiting", "Marcar esperando respuesta", "sent_to_area", "waiting_response"),
        ("receive_response", "Registrar respuesta recibida", "waiting_response", "quality_review"),
        ("approve_quality", "Aprobar calidad", "quality_review", "pending_signature"),
        ("mark_ready", "Marcar listo para responder", "pending_signature", "ready_to_answer"),
        ("answer_partial", "Registrar respuesta parcial", "ready_to_answer", "answered_partial"),
        ("answer_complete", "Registrar respuesta completa", "ready_to_answer", "answered_complete"),
        ("close_complete", "Cerrar", "answered_complete", "closed")
    ]

    for code, name, from_code, to_code in transitions_data:
        create_workflow_transition(
            db,
            {
                "process_id": process.id,
                "code": code,
                "name": name,
                "from_state_id": states[from_code].id,
                "to_state_id": states[to_code].id,
                "requires_comment": False,
                "requires_checklist_completed": False,
                "is_active": True
            }
        )

    requirement_doc = create_document_type(
        db,
        {
            "process_id": process.id,
            "code": "requirement_document",
            "name": "Requerimiento recibido",
            "description": "PDF, MSG, EML o documento original recibido.",
            "direction": "input",
            "allowed_extensions": "pdf,msg,eml,docx",
            "is_required": True,
            "is_ai_enabled": True
        }
    )

    area_response_doc = create_document_type(
        db,
        {
            "process_id": process.id,
            "code": "area_response",
            "name": "Respuesta del área",
            "description": "Respuesta recibida del área correspondiente.",
            "direction": "response",
            "allowed_extensions": "pdf,msg,eml,docx,xlsx,xls,csv",
            "is_required": False,
            "is_ai_enabled": True
        }
    )

    if02_doc = create_document_type(
        db,
        {
            "process_id": process.id,
            "code": "if02_excel",
            "name": "Excel IF02",
            "description": "Archivo Excel IF02 o estructura similar enviada por el área.",
            "direction": "response",
            "allowed_extensions": "xlsx,xls,csv",
            "is_required": False,
            "is_ai_enabled": True
        }
    )

    extraction_fields = [
        ("fecha_recepcion", "record", "received_date", "Extraer fecha de recepción o fecha del documento si está disponible."),
        ("numero_requerimiento", "record", "request_number", "Extraer número de oficio, comunicación o requerimiento."),
        ("originador", "record", "originator", "Extraer entidad, juzgado, tribunal o regulador que solicita."),
        ("origen", "record", "origin", "Clasificar origen: juzgado, tribunal, regulador, ministerio público u otro."),
        ("tipo_solicitud", "request_item", "request_type", "Identificar todas las solicitudes: certificación, inmovilización, descongelamiento, movimientos, estados de cuenta, etc."),
        ("identificacion", "person", "identification", "Extraer cédula, RNC, pasaporte u otra identificación si está disponible."),
        ("persona", "person", "full_name", "Extraer nombres de personas físicas o jurídicas mencionadas.")
    ]

    for source_name, target_entity, target_field, instructions in extraction_fields:
        create_extraction_field(
            db,
            {
                "document_type_id": requirement_doc.id,
                "source_name": source_name,
                "target_entity": target_entity,
                "target_field": target_field,
                "extraction_type": "ai",
                "is_required": False,
                "instructions": instructions
            }
        )

    excel_mappings = [
        ("Nombre", "person", "full_name"),
        ("Identificacion", "person", "identification"),
        ("Identificación", "person", "identification"),
        ("Producto", "request_item", "product"),
        ("Cuenta", "request_item", "account"),
        ("Estatus", "request_item", "status"),
        ("Observacion", "request_item", "pending_reason"),
        ("Observación", "request_item", "pending_reason")
    ]

    for column_name, target_entity, target_field in excel_mappings:
        create_excel_mapping(
            db,
            {
                "document_type_id": if02_doc.id,
                "sheet_name": None,
                "header_row": 1,
                "column_name": column_name,
                "target_entity": target_entity,
                "target_field": target_field,
                "is_required": False
            }
        )

    return {
        "status": "created",
        "message": "Proceso base de requerimientos regulatorios creado.",
        "process_id": process.id
    }
