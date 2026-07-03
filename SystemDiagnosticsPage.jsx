import { useEffect, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import StatusBadge from "../../components/ui/StatusBadge.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import { getSystemDiagnostics } from "./systemApi.js";

function SystemDiagnosticsPage() {
  const [diagnostics, setDiagnostics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadDiagnostics = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getSystemDiagnostics();
      setDiagnostics(response.data);
    } catch (err) {
      setError(err.message || "Error cargando diagnóstico");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDiagnostics();
  }, []);

  const countRows = diagnostics
    ? Object.entries(diagnostics.counts || {}).map(([key, value]) => ({
        id: key,
        metric: key,
        value,
      }))
    : [];

  const moduleRows = diagnostics
    ? Object.entries(diagnostics.modules || {}).map(([key, value]) => ({
        id: key,
        module: key,
        status: value ? "enabled" : "disabled",
      }))
    : [];

  return (
    <>
      <PageHeader
        title="Diagnóstico del sistema"
        description="Verificación rápida de base de datos, almacenamiento, módulos y conteos principales."
      />

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      {diagnostics && (
        <>
          <Card title="Estado general">
            <p>
              <strong>Estado:</strong>{" "}
              <StatusBadge value={diagnostics.status} />
            </p>

            <p>
              <strong>Base de datos:</strong>{" "}
              {diagnostics.database?.engine} / {diagnostics.database?.status}
            </p>

            <p>
              <strong>Uploads:</strong> {diagnostics.storage?.uploads_dir}
            </p>

            <p>
              <strong>Carpeta existe:</strong>{" "}
              {diagnostics.storage?.uploads_dir_exists ? "Sí" : "No"}
            </p>
          </Card>

          <Card title="Conteos">
            <DataTable
              columns={[
                { key: "metric", label: "Métrica" },
                { key: "value", label: "Valor" },
              ]}
              data={countRows}
              emptyMessage="Sin métricas."
            />
          </Card>

          <Card title="Módulos">
            <DataTable
              columns={[
                { key: "module", label: "Módulo" },
                {
                  key: "status",
                  label: "Estado",
                  render: (row) => <StatusBadge value={row.status} />,
                },
              ]}
              data={moduleRows}
              emptyMessage="Sin módulos."
            />
          </Card>
        </>
      )}
    </>
  );
}

export default SystemDiagnosticsPage;
