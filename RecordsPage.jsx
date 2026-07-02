import { useEffect, useMemo, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import DynamicForm from "../../components/forms/DynamicForm.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import {
  getProcesses,
  getProcessFields,
  getRecords,
  createRecord,
} from "./recordsApi.js";

import "../../components/forms/forms.css";

function RecordsPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");

  const [fields, setFields] = useState([]);
  const [records, setRecords] = useState([]);

  const [creating, setCreating] = useState(false);
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadProcesses = async () => {
    const response = await getProcesses();
    setProcesses(response.data);

    if (response.data.length && !selectedProcessId) {
      setSelectedProcessId(String(response.data[0].id));
    }
  };

  const loadProcessData = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const [fieldsResponse, recordsResponse] = await Promise.all([
        getProcessFields(processId),
        getRecords(processId),
      ]);

      setFields(fieldsResponse.data);
      setRecords(recordsResponse.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProcesses();
  }, []);

  useEffect(() => {
    loadProcessData(selectedProcessId);
  }, [selectedProcessId]);

  const handleCreateRecord = async (values) => {
    await createRecord({
      process_id: Number(selectedProcessId),
      title,
      summary,
      source_channel: "manual",
      created_by: "user",
      values,
    });

    setTitle("");
    setSummary("");
    setCreating(false);
    loadProcessData(selectedProcessId);
  };

  const columns = useMemo(() => {
    const baseColumns = [
      { key: "id", label: "ID" },
      { key: "current_state_id", label: "Estado" },
      { key: "title", label: "Título" },
      {
        key: "is_complete",
        label: "Completo",
        render: (row) => (row.is_complete ? "Sí" : "No"),
      },
      {
        key: "has_pending_items",
        label: "Pendientes",
        render: (row) => (row.has_pending_items ? "Sí" : "No"),
      },
    ];

    const dynamicColumns = fields
      .filter((field) => field.is_visible !== false)
      .slice(0, 6)
      .map((field) => ({
        key: `field_${field.name}`,
        label: field.label,
        render: (row) => {
          const found = row.values?.find((item) => item.field_name === field.name);
          return found?.value ?? "";
        },
      }));

    return [...baseColumns, ...dynamicColumns];
  }, [fields]);

  return (
    <>
      <PageHeader
        title="Registros"
        description="Requerimientos/casos operativos generados por el workflow."
        actions={
          <Button onClick={() => setCreating((value) => !value)}>
            Nuevo registro
          </Button>
        }
      />

      <Card title="Proceso">
        <div className="simple-form">
          <label>
            Proceso
            <select
              value={selectedProcessId}
              onChange={(event) => setSelectedProcessId(event.target.value)}
            >
              <option value="">Seleccione...</option>
              {processes.map((process) => (
                <option key={process.id} value={process.id}>
                  {process.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </Card>

      {creating && (
        <Card title="Nuevo registro">
          <div className="simple-form">
            <label>
              Título
              <input
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Título o referencia del requerimiento"
              />
            </label>

            <label>
              Resumen
              <textarea
                value={summary}
                onChange={(event) => setSummary(event.target.value)}
              />
            </label>
          </div>

          <br />

          <DynamicForm
            fields={fields}
            onSubmit={handleCreateRecord}
            submitLabel="Crear registro"
          />
        </Card>
      )}

      <Card title="Registros">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={records}
            emptyMessage="No hay registros creados."
          />
        )}
      </Card>
    </>
  );
}

export default RecordsPage;
