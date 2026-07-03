import DataTable from "../../table/DataTable.jsx";
import { useWorkspace } from "../engine/WorkspaceContext.jsx";

function PeopleWidget() {
  const workspace = useWorkspace();
  const people = workspace.people || [];

  const columns = [
    { key: "id", label: "ID" },
    { key: "full_name", label: "Nombre" },
    { key: "identification", label: "Identificación" },
    { key: "identification_type", label: "Tipo ID" },
    { key: "role", label: "Rol" },
    { key: "notes", label: "Notas" },
  ];

  return (
    <DataTable
      columns={columns}
      data={people}
      emptyMessage="No hay personas registradas en este expediente."
    />
  );
}

export default PeopleWidget;
