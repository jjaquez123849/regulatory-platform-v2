import { registerWidget } from "./WidgetRegistry.js";

import AIWidget from "../widgets/AIWidget.jsx";
import TimelineWidget from "../widgets/TimelineWidget.jsx";
import LogWidget from "../widgets/LogWidget.jsx";
import DocumentsWidget from "../widgets/DocumentsWidget.jsx";
import TasksWidget from "../widgets/TasksWidget.jsx";
import QualityWidget from "../widgets/QualityWidget.jsx";

export function registerDefaultWidgets() {
  registerWidget("AI_SUMMARY", AIWidget);
  registerWidget("TIMELINE", TimelineWidget);
  registerWidget("LOG", LogWidget);
  registerWidget("DOCUMENTS", DocumentsWidget);
  registerWidget("TASKS", TasksWidget);
  registerWidget("QUALITY", QualityWidget);
}
