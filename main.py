from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

from app.models import (
    Process,
    ProcessField,
    FieldOption,
    WorkflowState,
    WorkflowTransition,
    WorkflowHistory,
    DocumentType,
    DocumentExtractionField,
    ExcelColumnMapping,
    Record,
    RecordValue,
    RecordPerson,
    RecordRequestItem,
    Document,
    DocumentExtractionResult,
    Task,
    AuditLog,
    ExtractionLearningExample,
    QualityReview,
    QualityIssue,
    AutomationRule,
    AutomationCondition,
    AutomationAction,
    Notification,
    AIConfiguration,
    DocumentUnderstandingResult,
    User,
    Role,
    Permission,
    Capability,
    RolePermission,
    RoleCapability,
    UserRole,
    Area,
    Team,
    UserTeam,
    UserSession,
)

from app.routes import (
    admin,
    document_admin,
    workflow_admin,
    seed,
    records,
    workflow,
    documents,
    document_processing,
    extraction,
    learning,
    quality,
    tasks,
    dashboard,
    log_view,
    automation_admin,
    automation,
    notifications,
    ai_admin,
    document_classification,
    document_understanding,
    system,
    auth,
    security_seed,
    iam,
)


app = FastAPI(
    title="Regulatory Platform V2",
    version="0.1.0",
    description="Plataforma BPM configurable con IA documental",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(security_seed.router)
app.include_router(iam.router)
app.include_router(admin.router)
app.include_router(document_admin.router)
app.include_router(workflow_admin.router)
app.include_router(seed.router)
app.include_router(records.router)
app.include_router(workflow.router)
app.include_router(documents.router)
app.include_router(document_processing.router)
app.include_router(extraction.router)
app.include_router(learning.router)
app.include_router(quality.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)
app.include_router(log_view.router)
app.include_router(automation_admin.router)
app.include_router(automation.router)
app.include_router(notifications.router)
app.include_router(ai_admin.router)
app.include_router(document_classification.router)
app.include_router(document_understanding.router)
app.include_router(system.router)


@app.get("/")
def root():
    return {
        "application": "Regulatory Platform V2",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "sqlite",
        "configuration_source": "database",
        "auth_module": "enabled",
        "security_seed_module": "enabled",
        "iam_module": "enabled",
        "admin_module": "enabled",
        "document_admin_module": "enabled",
        "workflow_admin_module": "enabled",
        "seed_module": "enabled",
        "records_module": "enabled",
        "workflow_module": "enabled",
        "documents_module": "enabled",
        "document_processing_module": "enabled",
        "extraction_module": "enabled",
        "learning_module": "enabled",
        "quality_module": "enabled",
        "tasks_module": "enabled",
        "dashboard_module": "enabled",
        "log_view_module": "enabled",
        "automation_admin_module": "enabled",
        "automation_engine": "enabled",
        "notifications_module": "enabled",
        "ai_admin_module": "enabled",
        "document_classification_module": "enabled",
        "document_understanding_module": "enabled",
        "system_module": "enabled",
    }
