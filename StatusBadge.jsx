import "./ui.css";

const statusMap = {
  pending: "warning",
  in_progress: "info",
  completed: "success",
  cancelled: "muted",

  approved: "success",
  observed: "warning",
  incomplete: "danger",
  complete: "success",

  uploaded: "info",
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
  const statusClass = statusMap[value] || "muted";

  return (
    <span className={`status-badge status-${statusClass}`}>
      {value || "sin estado"}
    </span>
  );
}

export default StatusBadge;
