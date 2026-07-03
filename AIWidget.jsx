import { useState } from "react";

import Button from "../../ui/Button.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import AIInsightsPanel from "../AIInsightsPanel.jsx";
import { analyzeWorkspaceWithAI } from "../../../features/workspace/workspaceApi.js";

function AIWidget() {
  const workspace = useWorkspace();

  const latestUnderstanding = workspace.understandings?.[0];
  const recordId = workspace.record?.id;

  const defaultSummary =
    latestUnderstanding?.summary ||
    workspace.record?.summary ||
    "No hay resumen IA disponible.";

  const [analysis, setAnalysis] = useState("");
  const [running, setRunning] = useState(false);

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

  const handleAnalyze = async () => {
    if (!recordId) return;

    try {
      setRunning(true);

      const response = await analyzeWorkspaceWithAI(recordId);

      setAnalysis(response.data.analysis || "");
    } finally {
      setRunning(false);
    }
  };

  return (
    <>
      <div className="workspace-action-toolbar">
        <Button variant="secondary" onClick={handleAnalyze} disabled={running}>
          {running ? "Analizando..." : "Analizar expediente con IA local"}
        </Button>
      </div>

      <AIInsightsPanel
        summary={analysis || defaultSummary}
        insights={insights}
      />
    </>
  );
}

export default AIWidget;
