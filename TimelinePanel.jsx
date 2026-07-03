import "./workspace.css";

function TimelinePanel({ items = [] }) {
  if (!items.length) {
    return <p className="workspace-muted">No hay eventos en el timeline.</p>;
  }

  return (
    <div className="workspace-timeline">
      {items.map((item, index) => (
        <div key={item.id || index} className="workspace-timeline-item">
          <div className="workspace-timeline-dot" />

          <div>
            <strong>{item.title || item.action || "Evento"}</strong>
            {item.description && <p>{item.description}</p>}
            {item.date && <span>{item.date}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

export default TimelinePanel;
