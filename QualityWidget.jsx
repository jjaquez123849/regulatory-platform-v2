import DataTable from "../../table/DataTable.jsx";
import StatusBadge from "../../ui/StatusBadge.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";

function QualityWidget() {
  const workspace = useWorkspace();

  const issues = workspace.quality?.issues || [];
  const reviews = workspace.quality?.reviews || [];

  return (
    <>
      <h3>Revisiones</h3>

      <DataTable
        columns={[
          { key: "id", label: "ID" },
          {
            key: "status",
            label: "Estado",
            render: (row) => <StatusBadge value={row.status} />,
          },
          { key: "score", label: "Score" },
          { key: "summary", label: "Resumen" },
          { key: "reviewed_at", label: "Fecha" },
        ]}
        data={reviews}
        emptyMessage="No hay revisiones de calidad."
      />

      <br />

      <h3>Observaciones</h3>

      <DataTable
        columns={[
          { key: "id", label: "ID" },
          { key: "issue_type", label: "Tipo" },
          {
            key: "severity",
            label: "Severidad",
            render: (row) => <StatusBadge value={row.severity} />,
          },
          { key: "description", label: "Descripción" },
          {
            key: "is_resolved",
            label: "Resuelta",
            render: (row) => (row.is_resolved ? "Sí" : "No"),
          },
        ]}
        data={issues}
       
