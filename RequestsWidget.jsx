import DataTable from "../../table/DataTable.jsx";
import StatusBadge from "../../ui/StatusBadge.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";

function RequestsWidget() {
  const workspace = useWorkspace();
  const requestItems = workspace.request_items || [];

  const columns = [
    { key: "id", label: "ID" },
    { key: "person_id", label: "Persona" },
    { key: "request_type", label: "Tipo" },
    { key: "description", label: "Descripción" },
    {
      key: "status",
      label: "Estado",
      render: (row) => <StatusBadge value={row.status} />,
    },
    {
      key: "is_answered",
      label: "Respondido",
      render: (row) => (row.is_answered ? "Sí" : "No"),
    },
    { key: "pending_reason", label: "Pendiente" },
    { key: "response_summary", label: "Respuesta" },
  ];

  return (
    <DataTable
      columns={columns}
      data={requestItems}
      emptyMessage="No hay solicitudes registradas en este expediente."
    />
  );
}

export default RequestsWidget;
