import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";
import useApi from "../../hooks/useApi.js";

import {
  getDashboardSummary,
  getDashboardCritical,
} from "./dashboardApi.js";

import "./dashboard.css";

function DashboardPage() {
  const {
    data: summary,
    loading: summaryLoading,
    error: summaryError,
  } = useApi(getDashboardSummary, []);

  const {
    data: critical,
    loading: criticalLoading,
    error: criticalError,
  } = useApi(getDashboardCritical, []);

  const cards = [
    {
      label: "Registros",
      value: summary?.records_total ?? 0,
    },
    {
      label: "Abiertos",
      value: summary?.records_open ?? 0,
    },
    {
      label: "Completos",
      value: summary?.records_complete ?? 0,
    },
    {
      label: "Con pendientes",
      value: summary?.records_with_pending_items ?? 0,
    },
    {
      label: "Tareas pendientes",
      value: summary?.tasks_pending ?? 0,
    },
    {
      label: "Tareas vencidas",
      value: summary?.tasks_overdue ?? 0,
    },
    {
      label: "Observaciones calidad",
      value: summary?.quality_open_issues ?? 0,
    },
    {
      label: "Docs. por procesar",
      value: summary?.documents_pending_processing ?? 0,
    },
  ];

  const overdueTaskColumns = [
    { key: "record_id", label: "Registro" },
    { key: "title", label: "Tarea" },
    { key: "assigned_area", label: "Área" },
    { key: "assigned_to", label: "Asignado" },
    { key: "priority", label: "Prioridad" },
    { key: "due_date", label: "Vence" },
  ];

  const qualityColumns = [
    { key: "record_id", label: "Registro" },
    { key: "issue_type", label: "Tipo" },
    { key: "severity", label: "Severidad" },
    { key: "description", label: "Descripción" },
  ];

  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Centro operativo de requerimientos, tareas, documentos y calidad."
      />

      {summaryLoading && <LoadingState />}
      {summaryError && <ErrorState message={summaryError} />}

      {!summaryLoading && !summaryError && (
        <div className="metric-grid">
          {cards.map((card) => (
            <Card key={card.label}>
              <div className="metric-card">
                <span>{card.label}</span>
                <strong>{card.value}</strong>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Card title="Tareas vencidas">
        {criticalLoading && <LoadingState />}
        {criticalError && <ErrorState message={criticalError} />}
        {!criticalLoading && !criticalError && (
          <DataTable
            columns={overdueTaskColumns}
            data={critical?.overdue_tasks || []}
            emptyMessage="No hay tareas vencidas."
          />
        )}
      </Card>

      <Card title="Observaciones de calidad abiertas">
        {criticalLoading && <LoadingState />}
        {criticalError && <ErrorState message={criticalError} />}
        {!criticalLoading && !criticalError && (
          <DataTable
            columns={qualityColumns}
            data={critical?.quality_issues || []}
            emptyMessage="No hay observaciones abiertas."
          />
        )}
      </Card>
    </>
  );
}

export default DashboardPage;
