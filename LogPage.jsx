import { useEffect, useMemo, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import { getProcesses, getProcessLog } from "./logApi.js";

import "../../components/forms/forms.css";

function LogPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");
  const [rows, setRows] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadProcesses = async () => {
    const response = await getProcesses();
    setProcesses(response.data);

    if (response.data.length && !selectedProcessId) {
      setSelectedProcessId(String(response.data[0].id));
    }
  };

  const loadLog = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const response = await getProcessLog(processId);
      setRows(response.data);
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
    loadLog(selectedProcessId);
  }, [selectedProcessId]);

  const columns = useMemo(() => {
    const baseColumns = [
      { key: "record_id", label: "ID" },
      { key: "state", label: "Estado" },
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

    const firstRow = rows[0];

    if (!firstRow?.fields) {
      return baseColumns;
    }

    const dynamicColumns = Object.entries(firstRow.fields).map(
      ([fieldName, fieldInfo]) => ({
        key: `field_${fieldName}`,
        label: fieldInfo.label || fieldName,
        render: (row) => row.fields?.[fieldName]?.value ?? "",
      })
    );

    return [...baseColumns, ...dynamicColumns];
  }, [rows]);

  return (
    <>
      <PageHeader
        title="Log"
        description="Vista oficial de la base histórica. La base de datos es la única verdad."
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

      <Card title="Log dinámico">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={rows}
            emptyMessage="No hay registros en el log."
          />
        )}
      </Card>
    </>
  );
}

export default LogPage;
