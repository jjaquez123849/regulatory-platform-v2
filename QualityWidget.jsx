import Button from "../../ui/Button.jsx";
import DataTable from "../../table/DataTable.jsx";
import StatusBadge from "../../ui/StatusBadge.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { hasWorkspaceAction } from "../engine/WorkspacePermissions.js";

import {
  runQualityReview,
  resolveQualityIssue,
} from "../../../features/quality/qualityApi.js";

function QualityWidget() {
  const workspace = useWorkspace();

  const recordId = workspace.record?.id;
  const issues = workspace.quality?.issues || [];
  const reviews = workspace.quality?.reviews || [];

  const refresh = workspace.refreshWorkspace || (() => {});

  const handleRunQuality = async () => {
    if (!recordId) return;

    await runQualityReview(recordId);
    refresh();
  };

  const handleResolveIssue = async (issueId) => {
    await resolveQualityIssue(issueId, {
      resolved_by: "user",
      resolution_comment: "Resuelto desde Workspace.",
    });

    refresh();
  };

  return (
    <>
      {hasWorkspaceAction(workspace, "RUN_QUALITY") && (
        <div className="workspace-action-toolbar">
          <Button variant="secondary" onClick={handleRunQuality}>
            Ejecutar revisión
          </Button>
        </div>
      )}

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
          {
            key: "actions",
            label: "Acciones",
            render: (row) =>
              !row.is_resolved &&
              hasWorkspaceAction(workspace, "RESOLVE_QUALITY_ISSUE") ? (
                <Button
                  variant="secondary"
                  onClick={() => handleResolveIssue(row.id)}
                >
                  Resolver
                </Button>
              ) : (
                ""
              ),
          },
        ]}
        data={issues}
        emptyMessage="No hay observaciones de calidad."
      />
    </>
  );
}

export default QualityWidget;
