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
    ExcelColumnMapping
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
        "configuration_source": "database"
    }
