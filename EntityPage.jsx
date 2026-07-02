import { useState } from "react";

import PageHeader from "../ui/PageHeader.jsx";
import Card from "../ui/Card.jsx";
import Button from "../ui/Button.jsx";
import DataTable from "../table/DataTable.jsx";
import DynamicForm from "../forms/DynamicForm.jsx";
import LoadingState from "../feedback/LoadingState.jsx";
import ErrorState from "../feedback/ErrorState.jsx";

function EntityPage({
  title,
  description,
  createLabel = "Nuevo",
  listTitle = "Listado",
  formTitle = "Nuevo registro",
  fields = [],
  columns = [],
  data = [],
  loading = false,
  error = "",
  emptyMessage = "No hay datos.",
  onCreate,
  extraActions,
}) {
  const [creating, setCreating] = useState(false);

  const handleSubmit = async (values) => {
    await onCreate(values);
    setCreating(false);
  };

  return (
    <>
      <PageHeader
        title={title}
        description={description}
        actions={
          <>
            {extraActions}
            {onCreate && (
              <Button onClick={() => setCreating((value) => !value)}>
                {createLabel}
              </Button>
            )}
          </>
        }
      />

      {creating && (
        <Card title={formTitle}>
          <DynamicForm
            fields={fields}
            onSubmit={handleSubmit}
            submitLabel="Guardar"
          />
        </Card>
      )}

      <Card title={listTitle}>
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={data}
            emptyMessage={emptyMessage}
          />
        )}
      </Card>
    </>
  );
}

export default EntityPage;
