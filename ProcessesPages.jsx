import { useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";
import useApi from "../../../hooks/useApi.js";

import {
  getProcesses,
  createProcess,
  seedRegulatoryRequests,
} from "./processesApi.js";

function ProcessesPage() {
  const { data, loading, error, refetch } = useApi(getProcesses, []);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    code: "",
    name: "",
    description: "",
    is_default: false,
  });

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleCreate = async (event) => {
    event.preventDefault();

    await createProcess(form);

    setForm({
      code: "",
      name: "",
      description: "",
      is_default: false,
    });

    setCreating(false);
    refetch();
  };

  const handleSeed = async () => {
    await seedRegulatoryRequests();
    refetch();
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "code", label: "Código" },
    { key: "name", label: "Nombre" },
    { key: "description", label: "Descripción" },
    {
      key: "is_default",
      label: "Default",
      render: (row) => (row.is_default ? "Sí" : "No"),
    },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => (row.is_active ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Procesos"
        description="Administración de procesos configurables."
        actions={
          <>
            <Button variant="secondary" onClick={handleSeed}>
              Crear seed regulatorio
            </Button>
            <Button onClick={() => setCreating((value) => !value)}>
              Nuevo proceso
            </Button>
          </>
        }
      />

      {creating && (
        <Card title="Nuevo proceso">
          <form onSubmit={handleCreate} className="simple-form">
            <label>
              Código
              <input
                name="code"
                value={form.code}
                onChange={handleChange}
                placeholder="ej. regulatory_requests"
                required
              />
            </label>

            <label>
              Nombre
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="ej. Requerimientos Regulatorios"
                required
              />
            </label>

            <label>
              Descripción
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
              />
            </label>

            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_default"
                checked={form.is_default}
                onChange={handleChange}
              />
              Proceso por defecto
            </label>

            <div className="form-actions">
              <Button type="submit">Guardar</Button>
            </div>
          </form>
        </Card>
      )}

      <Card title="Procesos configurados">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}
        {!loading && !error && (
          <DataTable
            columns={columns}
            data={data || []}
            emptyMessage="No hay procesos configurados."
          />
        )}
      </Card>
    </>
  );
}

export default ProcessesPage;
