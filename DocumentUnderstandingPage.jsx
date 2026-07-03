import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import { getDocumentUnderstandingHistory } from "./documentsApi.js";

function DocumentUnderstandingPage() {
  const { documentId } = useParams();

  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getDocumentUnderstandingHistory(documentId);
      setItems(response.data);

      if (response.data.length) {
        setSelected(response.data[0]);
      }
    } catch (err) {
      setError(err.message || "Error cargando comprensión documental");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [documentId]);

  const columns = [
    { key: "id", label: "ID" },
    { key: "issuer", label: "Emisor" },
    { key: "regulator", label: "Regulador" },
    { key: "request_number", label: "No. Req." },
    { key: "due_date", label: "Plazo" },
    { key: "created_at", label: "Fecha" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) => (
        <button onClick={() => setSelected(row)}>
          Ver
        </button>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Comprensión documental"
        description={`Histórico de entendimiento del documento #${documentId}.`}
      />

      <Card title="Histórico">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={items}
            emptyMessage="No hay entendimientos guardados."
          />
        )}
      </Card>

      {selected && (
        <>
          <Card title="Resumen">
            <p><strong>Emisor:</strong> {selected.issuer || "No detectado"}</p>
            <p><strong>Regulador:</strong> {selected.regulator || "No detectado"}</p>
            <p><strong>No. requerimiento:</strong> {selected.request_number || "No detectado"}</p>
            <p><strong>Plazo:</strong> {selected.due_date || "No detectado"}</p>
            <p><strong>Resumen:</strong> {selected.summary || "Sin resumen"}</p>
          </Card>

          <Card title="Entidades detectadas">
            <DataTable
              columns={[
                { key: "entity_type", label: "Tipo" },
                { key: "value", label: "Valor" },
                { key: "confidence", label: "Confianza" },
              ]}
              data={selected.entities || []}
              emptyMessage="No hay entidades detectadas."
            />
          </Card>

          <Card title="Solicitudes detectadas">
            <DataTable
              columns={[
                { key: "description", label: "Descripción" },
                { key: "priority", label: "Prioridad" },
                { key: "due_date", label: "Plazo" },
              ]}
              data={selected.requests || []}
              emptyMessage="No hay solicitudes detectadas."
            />
          </Card>
        </>
      )}
    </>
  );
}

export default DocumentUnderstandingPage;
