import DataTable from "../table/DataTable.jsx";

function EditableGrid({
  columns = [],
  data = [],
  emptyMessage = "No hay datos.",
}) {
  return (
    <DataTable
      columns={columns}
      data={data}
      emptyMessage={emptyMessage}
    />
  );
}

export default EditableGrid;
