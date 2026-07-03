import "./workspace.css";

function SectionCard({ title, description, actions, children }) {
  return (
    <section className="workspace-section-card">
      <div className="workspace-section-header">
        <div>
          <h2>{title}</h2>
          {description && <p>{description}</p>}
        </div>

        {actions && (
          <div className="workspace-section-actions">
            {actions}
          </div>
        )}
      </div>

      <div className="workspace-section-body">
        {children}
      </div>
    </section>
  );
}

export default SectionCard;
