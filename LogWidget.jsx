import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import EditableGrid from "../EditableGrid.jsx";

function LogWidget() {
  const workspace = useWorkspace();

  const rows = workspace.values || [];

  const columns = [
    { key: "id", label: "ID" },
    { key: "field_id", label: "Campo" },
    { key: "value_text", label: "Texto" },
    { key: "value_number", label: "Número" },
    { key: "value_date", label: "Fecha" },
    {
      key: "value_boolean",
      label: "Booleano",
      render: (row) =>
        row.value_boolean === null || row.value_boolean === undefined
          ? ""
          : row.value_boolean
          ? "Sí"
          : "No",
    },
  ];

  return (
    <EditableGrid
      columns={columns}
      data={rows}
      emptyMessage="No hay valores del log."
    />
  );
}

export default LogWidget;
