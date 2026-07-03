import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import StatusBadge from "../../components/ui/StatusBadge.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import { getWorkQueues } from "./workQueuesApi.js";

function WorkQueuesPage() {
  const [queues, setQueues] = useState(null);
  const [selectedQueue, setSelectedQueue] = useState("my_tasks");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadQueues = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getWorkQueues();
      setQueues(response.data);
    } catch (err) {
      setError(err.message || "Error cargando bandejas");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQueues();
  }, []);

  const queueLabels = {
    my_tasks: "Mi trabajo",
    area_tasks: "Mi área",
    due_soon: "Por vencer",
    overdue: "Vencidos",
    quality_issues: "Calidad",
    pending_documents: "Documentos pendientes",
    open_records: "Expedientes abiertos",
  };

  const rows = queues?.[selectedQueue] || [];

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "record_id",
      label: "Expediente",
      render: (row) =>
        row.record_id ? (
          <Link to={`/records/${row.record_id}/workspace`}>
            #{row.record_id}
          </Link>
        ) : row.id ? (
          <Link to={`/records/${row.id}/workspace`}>
            #{row.id}
          </Link>
        ) : (
          ""
        ),
    },
    { key: "title", label: "Título" },
    { key: "description", label: "Descripción" },
    { key: "assigned_area", label: "Área" },
    { key: "assigned_to", label: "Asignado" },
    {
      key: "status",
      label: "Estado",
      render: (row) => row.status ? <StatusBadge value={row.status} /> : "",
    },
    {
      key: "priority",
      label: "Prioridad",
      render: (row) => row.priority ? <StatusBadge value={row.priority} /> : "",
    },
    { key: "due_date", label: "Vence" },
    { key: "processing_status", label: "Doc. Estado" },
    { key: "updated_at", label: "Actualizado" },
  ];

  return (
    <>
      <PageHeader
        title="Bandejas"
        description="Trabajo operativo por usuario, área, vencimiento, calidad y documentos pendientes."
      />

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      {queues && (
        <>
          <div className="admin-grid">
            {Object.entries(queueLabels).map(([key, label]) => (
              <Card key={key} title={label}>
                <h2>{queues.summary?.[key] ?? 0}</h2>
                <button onClick={() => setSelectedQueue(key)}>
                  Ver bandeja
                </button>
              </Card>
            ))}
          </div>

          <Card title={queueLabels[selectedQueue]}>
            <DataTable
              columns={columns}
              data={rows}
              emptyMessage="No hay elementos en esta bandeja."
            />
          </Card>
        </>
      )}
    </>
  );
}

export default WorkQueuesPage;
