import { useEffect, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import {
  getRecords,
  runQualityReview,
  getQualityReviews,
  getQualityIssues,
  resolveQualityIssue,
} from "./qualityApi.js";

import "../../components/forms/forms.css";

function QualityPage() {
  const [records, setRecords] = useState([]);
  const [selectedRecordId, setSelectedRecordId] = useState("");

  const [reviews, setReviews] = useState([]);
  const [issues, setIssues] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadRecords = async () => {
    const response = await getRecords();
    setRecords(response.data);

    if (response.data.length && !selectedRecordId) {
      setSelectedRecordId(String(response.data[0].id));
    }
  };

  const loadQualityData = async (recordId) => {
    if (!recordId) return;

    try {
      setLoading(true);
      setError("");

      const [reviewsResponse, issuesResponse] = await Promise.all([
        getQualityReviews(recordId),
        getQualityIssues(recordId),
      ]);

      setReviews(reviewsResponse.data);
      setIssues(issuesResponse.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecords();
  }, []);

  useEffect(() => {
    loadQualityData(selectedRecordId);
  }, [selectedRecordId]);

  const handleRunReview = async () => {
    await runQualityReview(selectedRecordId);
    loadQualityData(selectedRecordId);
  };

  const handleResolveIssue = async (issueId) => {
    await resolveQualityIssue(issueId, {
      resolved_by: "user",
      resolution_comment: "Resuelto desde la interfaz.",
    });

    loadQualityData(selectedRecordId);
  };

  const reviewColumns = [
    { key: "id", label: "ID" },
    { key: "status", label: "Estado" },
    { key: "score", label: "Resultado" },
    { key: "summary", label: "Resumen" },
    {
      key: "has_missing_items",
      label: "Faltantes",
      render: (row) => (row.has_missing_items ? "Sí" : "No"),
    },
    { key: "reviewed_at", label: "Fecha" },
  ];

  const issueColumns = [
    { key: "id", label: "ID" },
    { key: "issue_type", label: "Tipo" },
    { key: "severity", label: "Severidad" },
    { key: "description", label: "Descripción" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) =>
        row.is_resolved ? (
          "Resuelta"
        ) : (
          <Button variant="secondary" onClick={() => handleResolveIssue(row.id)}>
            Resolver
          </Button>
        ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Control de calidad"
        description="Verifica si las solicitudes fueron respondidas y detecta faltantes."
        actions={
          <Button onClick={handleRunReview} disabled={!selectedRecordId}>
            Ejecutar revisión
          </Button>
        }
      />

      <Card title="Registro">
        <div className="simple-form">
          <label>
            Registro
            <select
              value={selectedRecordId}
              onChange={(event) => setSelectedRecordId(event.target.value)}
            >
              <option value="">Seleccione...</option>
              {records.map((record) => (
                <option key={record.id} value={record.id}>
                  #{record.id} - {record.title || "Sin título"}
                </option>
              ))}
            </select>
          </label>
        </div>
      </Card>

      <Card title="Revisiones realizadas">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={reviewColumns}
            data={reviews}
            emptyMessage="No hay revisiones de calidad."
          />
        )}
      </Card>

      <Card title="Observaciones abiertas">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={issueColumns}
            data={issues}
            emptyMessage="No hay observaciones abiertas."
          />
        )}
      </Card>
    </>
  );
}

export default QualityPage;
