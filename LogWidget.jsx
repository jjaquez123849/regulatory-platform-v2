import { useState } from "react";

import Button from "../../ui/Button.jsx";
import DataTable from "../../table/DataTable.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { hasWorkspaceAction } from "../engine/WorkspacePermissions.js";
import { updateRecordLogValues } from "../../../features/workspace/workspaceApi.js";

import "../../../components/forms/forms.css";

function LogWidget() {
  const workspace = useWorkspace();

  const recordId = workspace.record?.id;
  const rows = workspace.values || [];
  const refresh = workspace.refreshWorkspace || (() => {});

  const canEdit = hasWorkspaceAction(workspace, "EDIT_LOG");

  const [editing, setEditing] = useState(false);
  const [values, setValues] = useState({});
  const [saving, setSaving] = useState(false);

  const getDisplayValue = (row) => {
    if (row.value_text !== null && row.value_text !== undefined) return row.value_text;
    if (row.value_number !== null && row.value_number !== undefined) return row.value_number;
    if (row.value_date !== null && row.value_date !== undefined) return row.value_date;

    if (row.value_boolean !== null && row.value_boolean !== undefined) {
      return row.value_boolean ? "Sí" : "No";
    }

    return "";
  };

  const startEdit = () => {
    const initialValues = {};

    rows.forEach((row) => {
      initialValues[row.field_id] = getDisplayValue(row);
    });

    setValues(initialValues);
    setEditing(true);
  };

  const cancelEdit = () => {
    setEditing(false);
    setValues({});
  };

  const handleChange = (fieldId, value) => {
    setValues((current) => ({
      ...current,
      [fieldId]: value,
    }));
  };

  const handleSave = async () => {
    if (!recordId) return;

    try {
      setSaving(true);

      const payload = {
        values: Object.entries(values).map(([fieldId, value]) => ({
          field_id: Number(fieldId),
          value,
        })),
      };

      await updateRecordLogValues(recordId, payload);

      setEditing(false);
      setValues({});
      refresh();
    } finally {
      setSaving(false);
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "field_id", label: "Campo" },
    {
      key: "value",
      label: "Valor",
      render: (row) =>
        editing ? (
          <input
            value={values[row.field_id] ?? ""}
            onChange={(event) => handleChange(row.field_id, event.target.value)}
          />
        ) : (
          getDisplayValue(row)
        ),
    },
  ];

  return (
    <>
      {canEdit && (
        <div className="workspace-action-toolbar">
          {!editing ? (
            <Button variant="secondary" onClick={startEdit}>
              Editar Log
            </Button>
          ) : (
            <>
              <Button onClick={handleSave} disabled={saving}>
                {saving ? "Guardando..." : "Guardar cambios"}
              </Button>

              <Button variant="secondary" onClick={cancelEdit} disabled={saving}>
                Cancelar
              </Button>
            </>
          )}
        </div>
      )}

      <DataTable
        columns={columns}
        data={rows}
        emptyMessage="No hay valores del log."
      />
    </>
  );
}

export default LogWidget;
