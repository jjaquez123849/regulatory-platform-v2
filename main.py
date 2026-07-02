from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

# =========================
# Models
# =========================

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
    AuditLog
)

# =========================
# Routes
# =========================

from app.routes import (
    admin,
    document_admin,
    workflow_admin
)


app = FastAPI(
    title="Regulatory Platform V2",
    version="0.1.0",
    description="Plataforma BPM configurable con IA documental"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(admin.router)
app.include_router(document_admin.router)
app.include_router(workflow_admin.router)


@app.get("/")
def root():
    return {
        "application": "Regulatory Platform V2",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "sqlite",
        "configuration_source": "database",
        "admin_module": "enabled",
        "document_admin_module": "enabled",
        "workflow_admin_module": "enabled"
    }
