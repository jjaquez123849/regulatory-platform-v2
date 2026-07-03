import { registerWidget } from "./WidgetRegistry.js";

import AIWidget from "../widgets/AIWidget.jsx";
import TimelineWidget from "../widgets/TimelineWidget.jsx";
import LogWidget from "../widgets/LogWidget.jsx";

export function registerDefaultWidgets() {
  registerWidget("AI_SUMMARY", AIWidget);
  registerWidget("TIMELINE", TimelineWidget);
  registerWidget("LOG", LogWidget);
}
