import { registerWidgetManifest } from "./WidgetManifestRegistry.js";

export function registerDefaultWidgetManifests() {
  registerWidgetManifest("AI_SUMMARY", {
    widget: "AI_SUMMARY",
    title: "Resumen IA",
    version: "1.0",
    permissions: ["AI_VIEW"],
    actions: [],
  });

  registerWidgetManifest("TIMELINE", {
    widget: "TIMELINE",
    title: "Timeline",
    version: "1.0",
    permissions: ["RECORD_VIEW"],
    actions: [],
  });

  registerWidgetManifest("LOG", {
    widget: "LOG",
    title: "Log",
    version: "1.0",
    permissions: ["RECORD_VIEW"],
    actions: ["EDIT_LOG"],
  });

  registerWidgetManifest("PEOPLE", {
    widget: "PEOPLE",
    title: "Personas",
    version: "1.0",
    permissions: ["RECORD_VIEW"],
    actions: [],
  });

  registerWidgetManifest("REQUESTS", {
    widget: "REQUESTS",
    title: "Solicitudes",
    version: "1.0",
    permissions: ["RECORD_VIEW"],
    actions: [],
  });

  registerWidgetManifest("DOCUMENTS", {
    widget: "DOCUMENTS",
    title: "Documentos",
    version: "1.0",
    permissions: ["DOCUMENT_VIEW"],
    actions: [
      "UPLOAD_DOCUMENT",
      "CLASSIFY_DOCUMENT",
      "UNDERSTAND_DOCUMENT",
      "PROCESS_DOCUMENT",
    ],
  });

  registerWidgetManifest("TASKS", {
    widget: "TASKS",
    title: "Tareas",
    version: "1.0",
    permissions: ["TASK_VIEW"],
    actions: ["CREATE_TASK", "ASSIGN_TASK", "COMPLETE_TASK"],
  });

  registerWidgetManifest("QUALITY", {
    widget: "QUALITY",
    title: "Calidad",
    version: "1.0",
    permissions: ["QUALITY_VIEW"],
    actions: ["RUN_QUALITY", "RESOLVE_QUALITY_ISSUE"],
  });

  registerWidgetManifest("COMMENTS", {
    widget: "COMMENTS",
    title: "Comentarios",
    version: "1.0",
    permissions: ["RECORD_VIEW"],
    actions: ["CREATE_COMMENT"],
  });

  registerWidgetManifest("AUDIT", {
    widget: "AUDIT",
    title: "Auditoría",
    version: "1.0",
    permissions: ["AUDIT_VIEW"],
    actions: [],
  });
}
