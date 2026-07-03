import { Link } from "react-router-dom";

import Button from "../../ui/Button.jsx";
import DataTable from "../../table/DataTable.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { hasWorkspaceAction } from "../engine/WorkspacePermissions.js";

import {
  classifyDocument,
  understandDocument,
  processDocument,
} from "../../../features/documents/documentsApi.js";

function DocumentsWidget() {
  const workspace = useWorkspace();
  const documents = workspace.documents || [];

  const refresh = workspace.refreshWorkspace || (() => {});

  const handleClassify = async (documentId) => {
    await classifyDocument(documentId);
    refresh();
  };

  const handleUnderstand = async (documentId) => {
    await understandDocument(documentId);
    refresh();
  };

  const handleProcess = async (documentId) => {
    await processDocument(documentId);
    refresh();
  };

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
            <Button variant="secondary" onClick={() => handleClassify(row.id)}>
              Clasificar
            </Button>
          )}

          {hasWorkspaceAction(workspace, "UNDERSTAND_DOCUMENT") && (
            <Button variant="secondary" onClick={() => handleUnderstand(row.id)}>
              Entender
            </Button>
          )}

          {hasWorkspaceAction(workspace, "PROCESS_DOCUMENT") && (
            <Button variant="secondary" onClick={() => handleProcess(row.id)}>
              Procesar
            </Button>
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
