import StatusBadge from "../ui/StatusBadge.jsx";
import "./workspace.css";

function WorkspaceHeader({
  title,
  subtitle,
  status,
  priority,
  assignedTo,
  actions,
}) {
  return (
    <div className="workspace-header">
      <div>
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>

      <div className="workspace-header-meta">
        {status && <StatusBadge value={status} />}
        {priority && <StatusBadge value={priority} />}

        {assignedTo && (
          <span className="workspace-assigned">
            Asignado: {assignedTo}
          </span>
        )}

        {actions && (
          <div className="workspace-header-actions">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
}

export default WorkspaceHeader;
