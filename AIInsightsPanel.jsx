import "./workspace.css";

function AIInsightsPanel({ summary, insights = [] }) {
  return (
    <div className="workspace-ai-panel">
      {summary && (
        <div className="workspace-ai-summary">
          <strong>Resumen IA</strong>
          <p>{summary}</p>
        </div>
      )}

      {insights.length > 0 ? (
        <ul>
          {insights.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="workspace-muted">No hay hallazgos IA disponibles.</p>
      )}
    </div>
  );
}

export default AIInsightsPanel;
