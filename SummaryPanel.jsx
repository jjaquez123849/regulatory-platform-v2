import "./workspace.css";

function SummaryPanel({ summary, emptyMessage = "No hay resumen disponible." }) {
  return (
    <div className="workspace-summary-panel">
      {summary ? <p>{summary}</p> : <p className="workspace-muted">{emptyMessage}</p>}
    </div>
  );
}

export default SummaryPanel;
