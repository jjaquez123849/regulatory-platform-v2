import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import AIInsightsPanel from "../AIInsightsPanel.jsx";

function AIWidget() {
  const workspace = useWorkspace();

  const latestUnderstanding = workspace.understandings?.[0];

  const summary =
    latestUnderstanding?.summary ||
    workspace.record?.summary ||
    "No hay resumen IA disponible.";

  const insights = [];

  if (latestUnderstanding?.issuer) {
    insights.push(`Emisor detectado: ${latestUnderstanding.issuer}`);
  }

  if (latestUnderstanding?.regulator) {
    insights.push(`Regulador detectado: ${latestUnderstanding.regulator}`);
  }

  if (latestUnderstanding?.due_date) {
    insights.push(`Plazo detectado: ${latestUnderstanding.due_date}`);
  }

  return (
    <AIInsightsPanel
      summary={summary}
      insights={insights}
    />
  );
}

export default AIWidget;
