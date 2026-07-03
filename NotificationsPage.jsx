import { useEffect, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import StatusBadge from "../../components/ui/StatusBadge.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";
import "../../components/forms/forms.css";
import {
  getNotifications,
  markNotificationRead,
} from "./notificationsApi.js";

function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [status, setStatus] = useState("unread");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadNotifications = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getNotifications({
        status: status || undefined,
      });

      setNotifications(response.data);
    } catch (err) {
      setError(err.message || "Error cargando notificaciones");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNotifications();
  }, [status]);

  const handleMarkRead = async (notificationId) => {
    await markNotificationRead(notificationId);
    loadNotifications();
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "record_id", label: "Registro" },
    { key: "title", label: "Título" },
    { key: "message", label: "Mensaje" },
    {
      key: "priority",
      label: "Prioridad",
      render: (row) => <StatusBadge value={row.priority} />,
    },
    {
      key: "status",
      label: "Estado",
      render: (row) => <StatusBadge value={row.status} />,
    },
    { key: "recipient_area", label: "Área" },
    { key: "created_at", label: "Fecha" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) =>
        row.status !== "read" ? (
          <Button variant="secondary" onClick={() => handleMarkRead(row.id)}>
            Marcar leída
          </Button>
        ) : (
          "Leída"
        ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Notificaciones"
        description="Alertas generadas por automatizaciones, calidad, documentos y workflow."
      />

      <Card title="Filtro">
        <div className="simple-form">
          <label>
            Estado
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
            >
              <option value="">Todas</option>
              <option value="unread">No leídas</option>
              <option value="read">Leídas</option>
            </select>
          </label>
        </div>
      </Card>

      <Card title="Notificaciones">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={notifications}
            emptyMessage="No hay notificaciones."
          />
        )}
      </Card>
    </>
  );
}

export default NotificationsPage;
