import { useState } from "react";

import Button from "../../ui/Button.jsx";
import DataTable from "../../table/DataTable.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { hasWorkspaceAction } from "../engine/WorkspacePermissions.js";
import { createComment } from "../../../features/comments/commentsApi.js";

import "../../../components/forms/forms.css";

function CommentsWidget() {
  const workspace = useWorkspace();

  const recordId = workspace.record?.id;
  const comments = workspace.comments || [];
  const refresh = workspace.refreshWorkspace || (() => {});

  const [commentText, setCommentText] = useState("");
  const [commentType, setCommentType] = useState("general");
  const [saving, setSaving] = useState(false);

  const canCreateComment = hasWorkspaceAction(workspace, "CREATE_COMMENT");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!recordId || !commentText.trim()) {
      return;
    }

    try {
      setSaving(true);

      await createComment({
        record_id: recordId,
        comment_text: commentText.trim(),
        comment_type: commentType,
      });

      setCommentText("");
      setCommentType("general");
      refresh();
    } finally {
      setSaving(false);
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "comment_type", label: "Tipo" },
    { key: "comment_text", label: "Comentario" },
    { key: "created_by", label: "Usuario" },
    { key: "created_at", label: "Fecha" },
  ];

  return (
    <>
      {canCreateComment && (
        <form onSubmit={handleSubmit} className="simple-form">
          <label>
            Tipo
            <select
              value={commentType}
              onChange={(event) => setCommentType(event.target.value)}
            >
              <option value="general">General</option>
              <option value="quality">Calidad</option>
              <option value="follow_up">Seguimiento</option>
              <option value="internal">Interno</option>
            </select>
          </label>

          <label>
            Comentario
            <textarea
              value={commentText}
              onChange={(event) => setCommentText(event.target.value)}
              placeholder="Escriba una nota interna del expediente..."
            />
          </label>

          <div className="form-actions">
            <Button type="submit" disabled={saving}>
              {saving ? "Guardando..." : "Agregar comentario"}
            </Button>
          </div>
        </form>
      )}

      <br />

      <DataTable
        columns={columns}
        data={comments}
        emptyMessage="No hay comentarios en este expediente."
      />
    </>
  );
}

export default CommentsWidget;
