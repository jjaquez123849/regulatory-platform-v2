from enum import Enum


class AutomationEvent(str, Enum):

    # =============================
    # Documentos
    # =============================

    DOCUMENT_UPLOADED = "document_uploaded"

    DOCUMENT_PROCESSED = "document_processed"

    EXTRACTION_COMPLETED = "extraction_completed"

    EXTRACTION_APPROVED = "extraction_approved"

    RESPONSE_DOCUMENT_RECEIVED = "response_document_received"

    # =============================
    # Registros
    # =============================

    RECORD_CREATED = "record_created"

    RECORD_UPDATED = "record_updated"

    RECORD_COMPLETED = "record_completed"

    # =============================
    # Workflow
    # =============================

    WORKFLOW_CHANGED = "workflow_changed"

    STATE_ENTERED = "state_entered"

    STATE_LEFT = "state_left"

    # =============================
    # Calidad
    # =============================

    QUALITY_STARTED = "quality_started"

    QUALITY_COMPLETED = "quality_completed"

    QUALITY_FAILED = "quality_failed"

    # =============================
    # IA
    # =============================

    AI_FINISHED = "ai_finished"

    AI_LOW_CONFIDENCE = "ai_low_confidence"

    # =============================
    # SLA
    # =============================

    SLA_WARNING = "sla_warning"

    SLA_EXPIRED = "sla_expired"

    # =============================
    # Manual
    # =============================

    BUTTON_EXECUTED = "button_executed"

    SCHEDULED = "scheduled"
