import { Link } from "react-router-dom";

import Button from "../../ui/Button.jsx";
import DataTable from "../../table/DataTable.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { hasWorkspaceAction } from "../engine/WorkspacePermissions.js";

function DocumentsWidget() {
  const workspace = useWorkspace();
  const documents = workspace.documents || [];

  const columns = [
    { key: "id", label: "ID" },
    { key: "original_filename", label: "Archivo" },
    { key: "file_extension", label: "Ext." },
    { key: "direction", label: "Dirección" },
    { key: "processing_status", label: "Estado" },
    { key: "uploaded_at", label: "Cargado" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) => (
        <div className="row-actions">
          {hasWorkspaceAction(workspace, "CLASSIFY_DOCUMENT") && (
            <Button variant="secondary">Clasificar</Button>
          )}

          {hasWorkspaceAction(workspace, "UNDERSTAND_DOCUMENT") && (
            <Button variant="secondary">Entender</Button>
          )}

          {hasWorkspaceAction(workspace, "PROCESS_DOCUMENT") && (
            <Button variant="secondary">Procesar</Button>
          )}

          <Link to={`/documents/${row.id}/understanding`}>
            Comprensión
          </Link>

          <Link to={`/documents/${row.id}/extraction`}>
            Extracción
          </Link>
        </div>
      ),
    },
  ];

  return (
    <DataTable
      columns={columns}
      data={documents}
      emptyMessage="No hay documentos en este expediente."
    />
  );
}

export default DocumentsWidget;
