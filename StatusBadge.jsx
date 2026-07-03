import "./ui.css";

const statusMap = {
  ok: "success",
  warning: "warning",
  error: "danger",

  enabled: "success",
  disabled: "muted",

  pending: "warning",
  in_progress: "info",
  completed: "success",
  cancelled: "muted",

  approved: "success",
  observed: "warning",
  incomplete: "danger",
  complete: "success",

  uploaded: "info",
  classified: "info",
  understood: "success",
  excel_extracted: "success",
  pdf_extracted: "success",
  text_extracted: "success",
  unsupported_for_now: "muted",

  unread: "warning",
  read: "success",

  low: "muted",
  medium: "info",
  high: "danger",
};

function StatusBadge({ value }) {
  const normalized = String(value || "sin estado");
  const statusClass = statusMap[normalized] || "muted";

  return (
    <span className={`status-badge status-${statusClass}`}>
      {normalized}
    </span>
  );
}

export default StatusBadge;
