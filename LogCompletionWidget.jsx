import { useEffect, useState } from "react";

import DataTable from "../../table/DataTable.jsx";
import StatusBadge from "../../ui/StatusBadge.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { getLogCompletion } from "../../../features/workspace/workspaceApi.js";

function LogCompletionWidget() {
  const workspace = useWorkspace();
  const recordId = workspace.record?.id;

  const [completion, setCompletion] = useState(null);
  const [error, setError] = useState("");

  const loadCompletion = async () => {
    if (!recordId) return;

    try {
      setError("");
      const response = await getLogCompletion(recordId);
      setCompletion(response.data);
    } catch (err) {
      setError(err.message || "Error cargando completitud del log");
    }
  };

  useEffect(() => {
    loadCompletion();
  }, [recordId]);

  if (error) {
    return <p className="workspace-muted">{error}</p>;
  }

  if (!completion) {
    return <p className="workspace-muted">Cargando estado del Log...</p>;
  }

  return (
    <>
      <div className="workspace-action-toolbar">
        <StatusBadge value={completion.is_complete ? "complete" : "incomplete"} />

        <span>
          Completados: {completion.completed_count} / {completion.total_fields}
        </span>

        <span>
          Faltantes requeridos: {completion.missing_required_count}
        </span>
      </div>

      <DataTable
        columns={[
          { key: "field_name", label: "Campo" },
          { key: "label", label: "Etiqueta" },
          { key: "data_type", label: "Tipo" },
          {
            key: "is_required",
            label: "Requerido",
            render: (row) => (row.is_required ? "Sí" : "No"),
          },
        ]}
        data={completion.missing || []}
        emptyMessage="No hay campos requeridos faltantes."
      />
    </>
  );
}

export default LogCompletionWidget;
