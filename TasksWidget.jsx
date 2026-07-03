import Button from "../../ui/Button.jsx";
import DataTable from "../../table/DataTable.jsx";
import StatusBadge from "../../ui/StatusBadge.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import { hasWorkspaceAction } from "../engine/WorkspacePermissions.js";

function TasksWidget() {
  const workspace = useWorkspace();
  const tasks = workspace.tasks || [];

  const columns = [
    { key: "id", label: "ID" },
    { key: "title", label: "Tarea" },
    { key: "assigned_area", label: "Área" },
    { key: "assigned_to", label: "Asignado" },
    {
      key: "status",
      label: "Estado",
      render: (row) => <StatusBadge value={row.status} />,
    },
    {
      key: "priority",
      label: "Prioridad",
      render: (row) => <StatusBadge value={row.priority} />,
    },
    { key: "due_date", label: "Vence" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) =>
        row.status !== "completed" &&
        hasWorkspaceAction(workspace, "COMPLETE_TASK") ? (
          <Button variant="secondary">
            Completar
          </Button>
        ) : (
          ""
        ),
    },
  ];

  return (
    <DataTable
      columns={columns}
      data={tasks}
      emptyMessage="No hay tareas para este expediente."
    />
  );
}

export default TasksWidget;
