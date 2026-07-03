import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Button from "../../components/ui/Button.jsx";
import WorkspaceHeader from "../../components/workspace/WorkspaceHeader.jsx";
import WorkspaceLoader from "../../components/workspace/engine/WorkspaceLoader.jsx";

import { getRecordWorkspace } from "./workspaceApi.js";
import "./workspacePage.css";

function WorkspacePage() {
  const { recordId } = useParams();

  const [workspace, setWorkspace] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadWorkspace = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getRecordWorkspace(recordId);
      setWorkspace(response.data);
    } catch (err) {
      setError(err.message || "Error cargando expediente.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkspace();
  }, [recordId]);

  return (
    <div className="workspace-page">
      {workspace?.record && (
        <WorkspaceHeader
          title={workspace.record.title || `Expediente #${workspace.record.id}`}
          subtitle={`Proceso ${workspace.record.process_id} · Registro ${workspace.record.id}`}
          status={workspace.record.state || "sin estado"}
          priority={workspace.record.has_pending_items ? "high" : "medium"}
          actions={
            <Button variant="secondary" onClick={loadWorkspace}>
              Refrescar
            </Button>
          }
        />
      )}

      <WorkspaceLoader
        workspace={workspace}
        loading={loading}
        error={error}
      />
    </div>
  );
}

export default WorkspacePage;
