import DataTable from "../../table/DataTable.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";

function AuditWidget() {
  const workspace = useWorkspace();
  const audit = workspace.audit || [];

  const columns = [
    { key: "id", label: "ID" },
    { key: "entity_type", label: "Entidad" },
    { key: "entity_id", label: "ID Entidad" },
    { key: "action", label: "Acción" },
    { key: "details", label: "Detalle" },
    { key: "performed_by", label: "Usuario" },
    { key: "created_at", label: "Fecha" },
  ];

  return (
    <DataTable
      columns={columns}
      data={audit}
      emptyMessage="No hay auditoría disponible para este expediente."
    />
  );
}

export default AuditWidget;
