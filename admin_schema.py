from typing import Optional, List
from pydantic import BaseModel


# =========================
# Processes
# =========================

class ProcessCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_default: bool = False


class ProcessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class ProcessResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool
    is_default: bool

    class Config:
        from_attributes = True


# =========================
# Fields
# =========================

class ProcessFieldCreate(BaseModel):
    process_id: int
    name: str
    label: str
    field_type: str
    is_required: bool = False
    is_visible: bool = True
    is_editable: bool = True
    is_exportable: bool = True
    display_order: int = 0
    help_text: Optional[str] = None
    default_value: Optional[str] = None


class ProcessFieldUpdate(BaseModel):
    label: Optional[str] = None
    field_type: Optional[str] = None
    is_required: Optional[bool] = None
    is_visible: Optional[bool] = None
    is_editable: Optional[bool] = None
    is_exportable: Optional[bool] = None
    display_order: Optional[int] = None
    help_text: Optional[str] = None
    default_value: Optional[str] = None


class ProcessFieldResponse(BaseModel):
    id: int
    process_id: int
    name: str
    label: str
    field_type: str
    is_required: bool
    is_visible: bool
    is_editable: bool
    is_exportable: bool
    display_order: int
    help_text: Optional[str] = None
    default_value: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# Field Options
# =========================

class FieldOptionCreate(BaseModel):
    field_id: int
    value: str
    label: str
    display_order: int = 0
    is_active: bool = True


class FieldOptionUpdate(BaseModel):
    value: Optional[str] = None
    label: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class FieldOptionResponse(BaseModel):
    id: int
    field_id: int
    value: str
    label: str
    display_order: int
    is_active: bool

    class Config:
        from_attributes = True


# =========================
# Full Process Config
# =========================

class ProcessFullConfigResponse(BaseModel):
    process: ProcessResponse
    fields: List[ProcessFieldResponse]

# =========================
# Document Types
# =========================

class DocumentTypeCreate(BaseModel):
    process_id: int
    code: str
    name: str
    description: Optional[str] = None
    direction: str = "input"
    allowed_extensions: Optional[str] = None
    is_required: bool = False
    is_ai_enabled: bool = True


class DocumentTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    direction: Optional[str] = None
    allowed_extensions: Optional[str] = None
    is_required: Optional[bool] = None
    is_ai_enabled: Optional[bool] = None


class DocumentTypeResponse(BaseModel):
    id: int
    process_id: int
    code: str
    name: str
    description: Optional[str] = None
    direction: str
    allowed_extensions: Optional[str] = None
    is_required: bool
    is_ai_enabled: bool

    class Config:
        from_attributes = True


# =========================
# Document Extraction Fields
# =========================

class DocumentExtractionFieldCreate(BaseModel):
    document_type_id: int
    source_name: str
    target_entity: str
    target_field: str
    extraction_type: str = "ai"
    is_required: bool = False
    instructions: Optional[str] = None


class DocumentExtractionFieldUpdate(BaseModel):
    source_name: Optional[str] = None
    target_entity: Optional[str] = None
    target_field: Optional[str] = None
    extraction_type: Optional[str] = None
    is_required: Optional[bool] = None
    instructions: Optional[str] = None


class DocumentExtractionFieldResponse(BaseModel):
    id: int
    document_type_id: int
    source_name: str
    target_entity: str
    target_field: str
    extraction_type: str
    is_required: bool
    instructions: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# Excel Column Mappings
# =========================

class ExcelColumnMappingCreate(BaseModel):
    document_type_id: int
    sheet_name: Optional[str] = None
    header_row: int = 1
    column_name: str
    target_entity: str
    target_field: str
    is_required: bool = False


class ExcelColumnMappingUpdate(BaseModel):
    sheet_name: Optional[str] = None
    header_row: Optional[int] = None
    column_name: Optional[str] = None
    target_entity: Optional[str] = None
    target_field: Optional[str] = None
    is_required: Optional[bool] = None


class ExcelColumnMappingResponse(BaseModel):
    id: int
    document_type_id: int
    sheet_name: Optional[str] = None
    header_row: int
    column_name: str
    target_entity: str
    target_field: str
    is_required: bool

    class Config:
        from_attributes = True

# =========================
# Workflow States
# =========================

class WorkflowStateCreate(BaseModel):
    process_id: int
    code: str
    name: str
    display_order: int = 0
    color: Optional[str] = None
    is_initial: bool = False
    is_final: bool = False
    is_active: bool = True


class WorkflowStateUpdate(BaseModel):
    name: Optional[str] = None
    display_order: Optional[int] = None
    color: Optional[str] = None
    is_initial: Optional[bool] = None
    is_final: Optional[bool] = None
    is_active: Optional[bool] = None


class WorkflowStateResponse(BaseModel):
    id: int
    process_id: int
    code: str
    name: str
    display_order: int
    color: Optional[str] = None
    is_initial: bool
    is_final: bool
    is_active: bool

    class Config:
        from_attributes = True


# =========================
# Workflow Transitions
# =========================

class WorkflowTransitionCreate(BaseModel):
    process_id: int
    code: str
    name: str
    from_state_id: int
    to_state_id: int
    requires_comment: bool = False
    requires_checklist_completed: bool = False
    is_active: bool = True


class WorkflowTransitionUpdate(BaseModel):
    name: Optional[str] = None
    from_state_id: Optional[int] = None
    to_state_id: Optional[int] = None
    requires_comment: Optional[bool] = None
    requires_checklist_completed: Optional[bool] = None
    is_active: Optional[bool] = None


class WorkflowTransitionResponse(BaseModel):
    id: int
    process_id: int
    code: str
    name: str
    from_state_id: int
    to_state_id: int
    requires_comment: bool
    requires_checklist_completed: bool
    is_active: bool

    class Config:
        from_attributes = True

# =========================
# Automation Rules
# =========================

class AutomationRuleCreate(BaseModel):
    process_id: int
    code: str
    name: str
    description: Optional[str] = None
    trigger_event: str
    is_active: bool = True


class AutomationRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_event: Optional[str] = None
    is_active: Optional[bool] = None


class AutomationRuleResponse(BaseModel):
    id: int
    process_id: int
    code: str
    name: str
    description: Optional[str] = None
    trigger_event: str
    is_active: bool

    class Config:
        from_attributes = True


class AutomationConditionCreate(BaseModel):
    rule_id: int
    left_value: str
    operator: str
    right_value: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class AutomationActionCreate(BaseModel):
    rule_id: int
    action_type: str
    action_payload: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    
